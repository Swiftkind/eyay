from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
    )
import json

from .models import Bot, Knowledge
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
        return Knowledge.objects.filter(bot=self.kwargs['bot'])

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        return super(self.__class__, self).get_permissions() 

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
            bot=self.kwargs['pk']).order_by('id').values_list('statement', 'answer')
        
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
        statement_vectors = [parse_text(clean_text(statement)) for statement in statements]
        lemmatized_vectors = [' '.join([tok.lemma_ for tok in st_vector 
                                if tok.lemma_ != '-PRON-'])  for st_vector in statement_vectors]
        message = parse_text(clean_text(message))
        lemmatized_input = ' '.join([tok.lemma_ for tok in message if tok.lemma_ != '-PRON-'])

        # contextual and non-contextual similarity scores,
        # then join both as a set for each statement
        vector_scores = [round(message.similarity(st_vector).item(), 4) 
                            for st_vector in statement_vectors]
        edist_scores = [str_similarity(lemmatized_input, lm_vector) 
                            for lm_vector in lemmatized_vectors]
        vector_and_edist = [x for x in zip(vector_scores, edist_scores)]

        # look for statement in knowledge with highest similarity score,
        # considering both contextual and non-contextual scores
        # first store answer's index, later be converted to actual answer
        bot_response = {'response': 0, 'confidence': 0.0} 
        for index, score in enumerate(vector_and_edist):
            avg_score = (score[0]+score[1])/2.0

            if avg_score > bot_response['confidence']:
                bot_response = {'response': index, 'confidence': avg_score}        

            if avg_score == 1:
                break        

        if bot_response['confidence'] < 0.65:
            return Response(json.dumps({'response': 'I dont know a good answer for that, \
            teach me by entering the proper answer to the question/query above.'})
            , status=HTTP_200_OK)
        else:
            bot_response = {
                'response': answers[bot_response['response']], 
                'confidence': round(bot_response['confidence'] * 100, 2)
            } 
            return Response(json.dumps(bot_response), status=HTTP_200_OK)
