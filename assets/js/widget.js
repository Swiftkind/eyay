(function() {

var jQuery;
var params = document.currentScript;

if (window.jQuery === undefined || window.jQuery.fn.jquery !== '3.2.1') {
    var jquery_script_tag = document.createElement('script');
    jquery_script_tag.setAttribute("type","text/javascript");
    jquery_script_tag.setAttribute("src",
        "http://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js");
    jquery_script_tag.onload = main;
    document.head.appendChild(jquery_script_tag);
} else {
    jQuery = window.jQuery;
    main();
}

function main() { 
  $(document).ready(function() { 
    var bot = parseInt(params.getAttribute('data-bot'));
    var botDiv = $('<div/>', {id: 'botChatbox'}).appendTo('body');;
    if (botDiv != null && !isNaN(bot)) {
      botDiv = $(botDiv);
      var chatURL = 'https://chateyay.localtunnel.me/api/bots/'+bot+'/chat/';
      var knowledgeURL = 'https://chateyay.localtunnel.me/api/bots/'+bot+'/knowledges/';
      var teachReply = "I'll have to ask my creator's approval for this.";
      var html_url = "https://chateyay.localtunnel.me/api/bots/get_chatbox/";
      var data_message = params.getAttribute('data-message');
      var starting_message =  data_message == null ? "Hello" : data_message;

      $.ajax({
        type: 'GET',
        url: html_url,
        data: {'bot': bot},
        contentType: 'application/json',
        success: function(data) {
          bot = data.bot;
          for (css_url in data.css) {
            var css_link = $("<link>", { 
              rel: "stylesheet", 
              type: "text/css", 
              href: data.css[css_url] 
            });
            css_link.appendTo('head');
          }

          botDiv.html(data.html);

          for (js_url in data.js) {
            var js_link = $("<script>", { 
              type: "text/javascript", 
              src: data.js[js_url]
            });
            js_link.appendTo('body');
          }

          var $chatlog = $('#botpro-chat-history');
          var $input = $('#botpro_id_message');
          var $botName = $('#botpro-bot-name');
          var $statusText = $('#botpro-status-text');
          var chat_log = document.getElementById('botpro-chat-history');
          var needAnswer = false;
          var prev = '';

          function createRow(sender, text) {
            var new_chat_name = document.createElement('h5');
            if (sender == bot.name) new_chat_name.setAttribute("class", "botpro-h5 botpro-bot");
            else new_chat_name.setAttribute("class", "botpro-h5 botpro-user");
            new_chat_name.innerHTML = sender;

            var new_chat_message = document.createElement('p');
            new_chat_message.setAttribute("class", "botpro-p");
            new_chat_message.innerHTML = text;

            var new_chat = document.createElement('div');
            new_chat.setAttribute("class", "botpro-chat-message-content botpro-clearfix");
            new_chat.appendChild(new_chat_name);
            new_chat.appendChild(new_chat_message);

            var new_row = document.createElement('div');
            new_row.setAttribute("class", "botpro-chat-message botpro-clearfix");
            new_row.appendChild(new_chat);
            chat_log.appendChild(new_row);

            var message_divider = document.createElement('hr');
            message_divider.setAttribute("class", "botpro-hr");
            chat_log.appendChild(message_divider);
            chat_log.scrollTop = chat_log.scrollHeight;
          }

          $botName.html(bot.name);
          if (!bot.is_active || bot.is_archived) createRow(bot.name, "I'm sorry, but my creator" +
            " has set me to an inactive state :(");
          else {
            $statusText.html(bot.name + ' is active');
            createRow(bot.name, starting_message);
          }

          function submitInput() {
            var inputData = {
              'message': $input.val()
            };
            $input.val('');
            createRow('You', inputData.message);

            if (needAnswer) {
              $.ajax({
                type: 'POST',
                url: knowledgeURL,
                data: JSON.stringify({'statement': "" + prev, 'answer': "" + inputData.message, 'bot': bot.id}),
                contentType: 'application/json',
                success: function(response) {
                  createRow(bot.name, teachReply);
                },
                error: function(err) {
                  if (err.status == 403) createRow(bot.name, 'I\'m sorry but \
                    only my creator is allowed to teach me things.');
                }
              });
              needAnswer = false;
            } else {
              $.ajax({
                type: 'POST',
                url: chatURL,
                data: JSON.stringify(inputData),
                contentType: 'application/json',
                beforeSend: function() {
                  $statusText.html(bot.name + ' is typing...');
                },
                success: function(data) {
                  $statusText.html(bot.name + ' is active');
                  data = JSON.parse(data);
                  if (data.confidence == null && data.response == "I don't know a good answer for that," +
                   " teach me by entering the proper answer to the question/query above.") {
                    prev = inputData.message;
                    needAnswer = true;
                  }
                  createRow(bot.name, '' + data.response);
                },
                error: function(errorMessages) {
                  errorMessages = JSON.parse(errorMessages.responseJSON);
                  createRow(bot.name, errorMessages.details);
                }
              });
            }
          }

          $input.keydown(function(event) {
            if (event.keyCode == 13) {
              submitInput();
            }
          });          
        },
        error: function(errorMessages) {
          console.log(errorMessages);
        }
      });
    } else {
      alert('Bot chatbox cannot be shown because data-bot is not defined or has an invalid value');
    }
  });
}

})(); 