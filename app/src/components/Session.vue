<template>
  <div class="session" :class="[sessionToggleClass]">
    <div class="session__toggle" v-on:click="toggle">
      <svg class="session__toggle__icon" width="13px" height="8px" viewBox="0 0 13 8" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
          <title>Chevron Arrow</title>
          <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <g
                class="icon-chevron"
                transform="translate(1.000000, 1.000000)"
                fill="#000000"
                fill-rule="nonzero"
                stroke="#000000">
                  <path d="M10.9999998,5.50171717 C11.0000856,5.42490512 10.9695513,
                  5.35122694 10.9151566,5.29699308 L5.7029449,0.0847813876 C5.58986891,
                  -0.0282604625 5.40657271,-0.0282604625 5.29349672,0.0847813876 L0.0812850265,
                  5.29699308 C-0.0284529392,5.41061318 -0.0268835319,5.59121802 0.0848123689,
                  5.70291392 C0.19650827,5.81460982 0.37711311,5.81617923 0.490733212,
                  5.70644127 L5.49822081,0.698953665 L10.5057084,5.70644127 C10.588523,
                  5.78923085 10.7130492,5.81399291 10.8212368,5.76918413 C10.9294243,
                  5.72437534 10.9999748,5.61881701 10.9999998,5.50171717 Z"></path>
              </g>
          </g>
      </svg>
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
      this.$emit('session-toggle', {
        source: 'session',
        index: this.index,
        state: !this.isToggleOpen,
      });
    },
  },
};
</script>

<style lang="scss">
@import '../assets/styles/colors';
.session {
  overflow: hidden;

  &__toggle {
    padding: 10px;
    margin: 10px 0;
    border: 2px solid $color-dark-gray-faded;
    border-radius: 8px;
    color: $color-dark-gray-faded;
    cursor: pointer;

    .icon-chevron {
      fill: $color-dark-gray-faded;
      stroke: $color-dark-gray-faded;
    }

    .session__toggle__icon {
      transform: rotate(180deg);
      margin-right: 5px;
    }
  }

  &__messages {
    display: block;
    position: relative;
    margin: 0;
    padding: 0;
  }

  &--expanded &__toggle {
    font-weight: bold;
    color: $text-color;
    cursor: default;

    .session__toggle__icon {
      transform: rotate(0deg);
    }
  }

  &--collapsed &__toggle:hover {
    color: $text-color;

    .icon-chevron {
      fill: $text-color;
      stroke: $text-color;
    }
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
