<template>
  <div class="session" :class="[sessionToggleClass]">
    <div class="session__toggle" v-on:click="toggle()">
      {{ sessionNumber }}. Session
    </div>
    <transition name="slide-fade">
      <div class="session__messages" v-if="isToggleOpen">
        <Message
          v-for="(groupedMessages, index) in messagesFormatted"
          :key="index"
          v-bind:index="index"
          v-bind:messages="groupedMessages.messages"
          v-bind:sender="people[groupedMessages.sender]" />
      </div>
    </transition>
  </div>
</template>

<script>
import Message from './Message';

export default {
  name: 'Session',
  components: {
    Message,
  },
  props: {
    index: Number,
    session: Array,
    sessionNumber: String,
    people: Object,
    selected: Boolean,
  },
  data() {
    return {
      isToggleOpen: this.selected,
      toggleClasses: { open: 'expanded', closed: 'collapsed' },
    };
  },
  watch: {
    selected(newState) {
      this.isToggleOpen = newState;
    },
  },
  computed: {
    sessionToggleClass() {
      const toggleClass = this.isToggleOpen ? this.toggleClasses.open : this.toggleClasses.closed;
      return `session--${toggleClass}`;
    },
    messagesFormatted() {
      const messagesFormatted = [];

      this.session.forEach((message) => {
        const lastMessage = messagesFormatted[messagesFormatted.length - 1];

        if (typeof lastMessage === 'undefined' || message.sender !== lastMessage.sender) {
          const newMessage = Object.assign({}, message);
          newMessage.messages = [message.message_text];
          delete newMessage.message_text;

          messagesFormatted.push(newMessage);
        } else {
          lastMessage.messages.push(message.message_text);
        }
      });

      return messagesFormatted;
    },
  },
  methods: {
    toggle() {
      this.isToggleOpen = !this.isToggleOpen;
    },
  },
};
</script>

<style lang="scss">
$color-dark-gray: #222222;
$color-dark-gray-faded: rgba($color-dark-gray, 0.5);
$color-gray: #EEE;
.session {
  overflow: hidden;
  border-right: 1px solid $color-gray;

  &__toggle {
    padding: 10px;
    margin: 10px 0;
    border: 2px solid $color-dark-gray-faded;
    border-radius: 8px;
    color: $color-dark-gray-faded;
    cursor: pointer;
  }

  &__messages {
    display: block;
    position: relative;
    margin: 0;
    padding: 0;
  }

  &--expanded &__toggle {
    color: $color-dark-gray;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: all 300ms ease-in-out;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 300ms ease-in-out;
}
.slide-fade-enter,
.slide-fade-leave-to {
  opacity: 0;
  height: 50%;
  transform: scaleY(0.9);
}
</style>
