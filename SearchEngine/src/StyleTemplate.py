css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.mobilelive.ca/wp-content/uploads/2020/11/ml-logo.png" style="height: 78px; width: 78px; border-radius: 50%; object-fit: contain;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn0.iconfinder.com/data/icons/user-interface-user-experience-4-4/24/200-1024.png" style="height: 78px; width: 78px; border-radius: 50%; object-fit: contain;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''