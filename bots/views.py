from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import (
    Paginator, 
    EmptyPage, 
    PageNotAnInteger
    )

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
    )
from rest_framework.renderers import JSONRenderer

from datetime import datetime, timedelta
import json
import numpy
import string

from .models import Bot, Knowledge
from .mixins import UserIsOwnerMixin
from .serializers import (
    BotDetailsSerializer, 
    ArchivedBotSerializer,
    BotKnowledgeSerializer
    )
from .permissions import IsOwner
from .utils import parse_text, clean_text, str_similarity


class BotViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = BotDetailsSerializer
    queryset = Bot.objects.filter(is_archived=False)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(is_active=True)

    def perform_destroy(self, instance):
        instance.is_archived = True
        instance.save()


class ArchiveViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = ArchivedBotSerializer

    def get_queryset(self):
        return Bot.objects.filter(is_archived=True, creator=self.request.user)


class KnowledgeViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = BotKnowledgeSerializer

    def get_queryset(self):
        return Knowledge.objects.filter(bot=self.kwargs['bot']).order_by('id')

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        return super(self.__class__, self).get_permissions() 

    def create(self, request, *args, **kwargs):
        statement = request.data.get('statement')
        if statement:
            request.data['statement'] = statement.lower()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        bot = get_object_or_404(Bot, pk=self.kwargs['bot'])
        if self.request.user == bot.creator:
            serializer.save(bot=bot, is_accepted=True)
        serializer.save(bot=bot)
        

class ChatBot(APIView):
    def post(self, request, *args, **kwargs):
        message = self.request.data.get('message')
        if not message:
            return Response(json.dumps({'details': 'No message given'}), 
                status=HTTP_400_BAD_REQUEST)
        
        bot_knowledge = Knowledge.objects.filter(
            bot=self.kwargs['pk'], 
            is_accepted=True).order_by('id').values_list('statement', 'answer')
        suggested_knowledge = Knowledge.objects.filter(
            bot=self.kwargs['pk'], 
            is_accepted=False).order_by('id').values_list('statement')

        suggested_statements = []
        for line in suggested_knowledge:
            suggested_statements.append(line[0])
        
        # separate statements and answers from bot knowledge
        statements = []
        answers = []
        for line in bot_knowledge:
            statements.append(line[0])
            answers.append(line[1])

        # We create vectors for contextual comparison, using parse_text()
        # this uses spaCy's english corpus, then comparison 
        # will use spaCy's similarity().
        
        # We then lemmatize vectors for non-contextual comparison
        # which can be derived from the vectors, then comparison 
        # will use fuzzy matching and levenshtein algorithm
        statement_vectors = [parse_text(clean_text(statement, 1)) for statement in statements]
        statement_vectors_b = [parse_text(clean_text(statement)) for statement in statements]
        lemmatized_vectors = [''.join([tok.lemma_ if tok.lemma_ in string.punctuation 
                        else ' '+tok.lemma_ for tok in st_vector if tok.lemma_ 
                        != '-PRON-']).strip() for st_vector in statement_vectors_b]

        message_a = parse_text(clean_text(message, 1))
        message_b = parse_text(clean_text(message))
        lemmatized_input = ''.join([tok.lemma_ if tok.lemma_ in string.punctuation 
            else ' '+tok.lemma_ for tok in message_b if tok.lemma_ != '-PRON-']).strip()

        # contextual and non-contextual similarity scores,
        # then join both as a set for each statement

        # Note: spaCy will return a vector filled with 0s if the string to be
        # parsed is not a word, or not in the corpus' vocabulary, causing
        # .similarity() to return a Python float instead of a NumPy float 
        vector_scores = [0 if not isinstance(message_a.similarity(st_vector), numpy.float64)
                        else round(message_a.similarity(st_vector).item(), 4) 
                        for st_vector in statement_vectors]
        edist_scores = [str_similarity(lemmatized_input, lm_vector) 
                            for lm_vector in lemmatized_vectors]
        vector_and_edist = [x for x in zip(vector_scores, edist_scores)]

        # look for statement in knowledge with highest similarity score,
        # considering both contextual and non-contextual scores
        # first store answer's index, later be converted to actual answer
        bot_response = {'response': 0, 'confidence': 0.0} 
        for index, score in enumerate(vector_and_edist):
            print(score)
            if score[0] > 0:
                final_score = (score[0] * 0.7) + (score[1] * 0.3)
            else:
                final_score = score[1]

            if final_score > bot_response['confidence']:
                bot_response = {'response': index, 'confidence': final_score}

            if final_score == 1:
                bot_response = {'response': index, 'confidence': 1}
                break     

            if score[1] == 1:
                bot_response = {'response': index, 'confidence': 1}

        if bot_response['confidence'] < 0.65:
            if message in suggested_statements:
                return Response(json.dumps({'response': 'I have a pending query with the same \
            question you asked that needs to be accepted by my creator.'})
            , status=HTTP_200_OK)
            else:
                return Response(json.dumps({'response': 'I dont know a good answer for that, \
            teach me by entering the proper answer to the question/query above.'})
            , status=HTTP_200_OK)
        else:
            bot_response = {
                'response': answers[bot_response['response']], 
                'confidence': round(bot_response['confidence'] * 100, 2)
            } 
            return Response(json.dumps(bot_response), status=HTTP_200_OK)


class ChatBotAppView(TemplateView):
    template_name = "bots/chat.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['bot'] = get_object_or_404(Bot, pk=self.kwargs['pk'])
        return context


class IndexView(ListView):
    model = Bot
    context_object_name = 'bots'
    template_name = 'bots/index.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = self.model.objects.filter(is_archived=False).order_by('-id')
        status = self.request.GET.get('status')
        if status and status != 'None':
            if status.lower() in ('active', 'inactive'):
                status = True if status.lower() == 'active' else False
                queryset = queryset.filter(is_active=status)
            else:
                raise Http404('Invalid status ({0}): No results to show'.format(status))
        created = self.request.GET.get('created')
        if created and created != 'None':
            if created.lower() in ('week', 'month'):
                date_today = datetime.today()
                last_week = date_today - timedelta(days=7)
                last_month = date_today - timedelta(days=31)

                created = last_week if created == 'week' else last_month
                queryset = queryset.filter(created__gte=created)
            else:
                raise Http404('Invalid filter ({0}): No results to show'.format(status))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status')
        context['created'] = self.request.GET.get('created')
        context['total_bots'] = Bot.objects.filter(is_archived=False).count()
        context['active_bots'] = Bot.objects.filter(is_archived=False, is_active=True).count()
        return context


class AddChatBotView(TemplateView):
    template_name = "bots/addbot.html"


class BotDetailView(UserIsOwnerMixin, ListView):
    model = Knowledge
    context_object_name = 'bot_knowledge'
    template_name = 'bots/botdetails.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = self.model.objects.filter(
            is_accepted=True, bot=self.kwargs['pk']).order_by('-id')
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['bot'] = get_object_or_404(Bot, pk=self.kwargs['pk'])
        suggested_knowledge = self.model.objects.filter(
            is_accepted=False, bot=self.kwargs['pk']).order_by('id')
        p = self.request.GET.get('p')
        paginator_b = Paginator(suggested_knowledge, 5)

        try:
            suggestions = paginator_b.page(p) if p else paginator_b.page(1)
        except PageNotAnInteger:
            raise Http404('Page can not be converted to an int.')
        except EmptyPage:
            raise Http404('Invalid page ({}): That page contains no results'.format(p))

        context['page_a'] = context['page_obj'].number
        context['page_b'] = suggestions.number
        context['suggestions'] = suggestions
        context['num_pages_b'] = paginator_b.num_pages
        return context


class MyBots(LoginRequiredMixin, ListView):
    model = Bot
    context_object_name = 'bots'
    template_name = 'bots/mybots.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = self.model.objects.filter(
            creator=self.request.user, is_archived=False).order_by('-id')
        status = self.request.GET.get('status')
        if status and status != 'None':
            if status.lower() in ('active', 'inactive'):
                status = True if status.lower() == 'active' else False
                queryset = queryset.filter(is_active=status)
            else:
                raise Http404('Invalid status ({0}): No results to show'.format(status))
        created = self.request.GET.get('created')
        if created and created != 'None':
            if created.lower() in ('week', 'month'):
                date_today = datetime.today()
                last_week = date_today - timedelta(days=7)
                last_month = date_today - timedelta(days=31)

                created = last_week if created == 'week' else last_month
                queryset = queryset.filter(created__gte=created)
            else:
                raise Http404('Invalid filter ({0}): No results to show'.format(status))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['status'] = self.request.GET.get('status')
        context['created'] = self.request.GET.get('created')
        context['total_bots'] = Bot.objects.filter(creator=user, is_archived=False).count()
        context['active_bots'] = Bot.objects.filter(
            is_active=True, creator=user, is_archived=False).count()
        return context


class ArchivedBots(LoginRequiredMixin, ListView):
    model = Bot
    context_object_name = 'bots'
    template_name = 'bots/archive.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = self.model.objects.filter(
            creator=self.request.user, is_archived=True).order_by('-id')
        created = self.request.GET.get('created')
        if created and created != 'None':
            if created.lower() in ('week', 'month'):
                date_today = datetime.today()
                last_week = date_today - timedelta(days=7)
                last_month = date_today - timedelta(days=31)

                created = last_week if created == 'week' else last_month
                queryset = queryset.filter(created__gte=created)
            else:
                raise Http404('Invalid filter ({0}): No results to show'.format(status))
        return queryset
