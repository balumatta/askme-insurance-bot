<template>
  <div class="chatbot-wrapper">
    <div class="chatbot-container">
      <div class="chat-header">AskMe Insurance Bot</div>

      <div class="chat-window">
        <div class="message" v-for="(message, index) in messages" :key="index">
          <div class="bubble user">
            <strong>User:</strong> {{ message.query }}
          </div>

          <!-- Bot typing -->
          <div v-if="message.loading" class="bubble bot">
            <strong>Bot:</strong>
            <span class="dots"><span>.</span><span>.</span><span>.</span></span>
          </div>

          <!-- Bot response -->
          <div v-else-if="message.answer" class="bubble bot">
            <strong>Bot:</strong> {{ message.answer }}
          </div>

          <!-- Bot error -->
          <div v-else-if="message.error" class="bubble bot">
            <strong>Bot:</strong> {{ message.error }}
            <button class="retry-button" @click="retryMessage(index)">Retry</button>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="query"
          @keyup.enter="sendQuery"
          type="text"
          placeholder="Ask me anything..."
        />
        <button @click="sendQuery">Send</button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      query: "",
      messages: [],
    };
  },
  methods: {
    async sendQuery() {
      const userQuery = this.query.trim();
      if (!userQuery) return;

      this.query = "";

      const newMessage = {
        query: userQuery,
        answer: null,
        error: null,
        loading: true,
      };

      this.messages.push(newMessage);
      const index = this.messages.length - 1;

      try {
        const response = await fetch("https://13.233.201.110/api/bot/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: userQuery }),
        });

        const data = await response.json();
        this.messages[index].loading = false;

        if (data.code === 200) {
          this.messages[index].answer = data.answer_info.answer;
        } else {
          this.messages[index].error = "Oops! Couldn’t generate a response.";
        }
      } catch (error) {
        this.messages[index].loading = false;
        this.messages[index].error = "Server error. Try again?";
      }

      this.scrollToBottom();
    },

    async retryMessage(index) {
      const retryQuery = this.messages[index].query;

      this.messages[index] = {
        query: retryQuery,
        answer: null,
        error: null,
        loading: true,
      };

      try {
        const response = await fetch("http://localhost:9000/api/bot/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: retryQuery }),
        });

        const data = await response.json();
        this.messages[index].loading = false;

        if (data.code === 200) {
          this.messages[index].answer = data.answer_info.answer;
        } else {
          this.messages[index].error = "Still not working. Try again later.";
        }
      } catch (error) {
        this.messages[index].loading = false;
        this.messages[index].error = "No response. Internet tantrum maybe?";
      }

      this.scrollToBottom();
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const chatWindow = this.$el.querySelector(".chat-window");
        chatWindow.scrollTop = chatWindow.scrollHeight;
      });
    },
  },
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.chatbot-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #e3f2fd, #fce4ec);
  font-family: 'Inter', sans-serif;
  padding: 20px;
}

.chatbot-container {
  width: 100%;
  max-width: 600px;
  height: 80vh;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background-color: #6200ea;
  color: #fff;
  font-weight: 600;
  padding: 20px;
  text-align: center;
  font-size: 20px;
}

.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f5f5;
}

.message {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 20px;
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
  transition: all 0.3s ease;
}

.bubble.user {
  align-self: flex-end;
  background: #e3f2fd;
  color: #333;
  border-bottom-right-radius: 0;
}

.bubble.bot {
  align-self: flex-start;
  background: #ede7f6;
  color: #333;
  border-bottom-left-radius: 0;
}

.chat-input {
  display: flex;
  padding: 16px;
  background: #fafafa;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 12px 16px;
  border-radius: 30px;
  border: 1px solid #ccc;
  outline: none;
  transition: border 0.2s;
}

.chat-input input:focus {
  border-color: #6200ea;
}

.chat-input button {
  margin-left: 12px;
  padding: 12px 20px;
  border: none;
  border-radius: 30px;
  background-color: #6200ea;
  color: white;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.chat-input button:hover {
  background-color: #7c4dff;
}

/* Scrollbar styling */
.chat-window::-webkit-scrollbar {
  width: 6px;
}
.chat-window::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 4px;
}

/* Add below styles to your existing <style scoped> */

.bubble.bot .dots {
  display: inline-flex;
  gap: 4px;
}

.dots span {
  animation: blink 1.2s infinite;
  font-size: 20px;
  color: #999;
}

.dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0% { opacity: 0.2; }
  20% { opacity: 1; }
  100% { opacity: 0.2; }
}

.retry-button {
  display: inline-block;
  margin-top: 8px;
  padding: 6px 12px;
  background: #ff5252;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.2s ease;
}

.retry-button:hover {
  background: #e53935;
}

</style>
