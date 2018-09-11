<template>
  <li class="session" :class="[sessionToggleClass]" v-if="hasMessages">
    <transition name="animation-fade">
      <a
        class="session__toggle"
        :style="{ backgroundImage: 'url('+sessionHeader.image_url+')' }"
        v-on:click="toggle"
        v-on:keyup.enter="toggle()"
        :title="(isToggleOpen ? 'Close' : 'Open') + ' Session #' + sessionNumber"
        tabindex="0">
        <span class="session__toggle__contents">
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
          {{ sessionToggleText }}
        </span>
      </a>
    </transition>
    <ol class="session__messages" v-if="isToggleOpen">
      <Message
        v-for="(groupedMessages, index) in messagesFormatted"
        :key="index"
        v-bind:index="index"
        v-bind:messages="groupedMessages.messages"
        v-bind:sender="people[groupedMessages.sender]" />
    </ol>
  </li>
  <li class="session session--disabled" v-else>
    <span class="session__toggle">{{ sessionNumber }}. Session</span>
  </li>
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
    sessionHeader: Object,
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
    hasMessages() {
      return typeof this.session !== 'undefined'
            && this.session !== null
            && this.session.length > 0;
    },
    messagesFormatted() {
      const messagesFormatted = [];

      if (!this.hasMessages) {
        return [];
      }

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
    sessionToggleText() {
      return (this.isToggleOpen) ? `${this.sessionNumber}. ${this.sessionHeader.title}` : `${this.sessionNumber}. Session`;
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
@import '../assets/styles/toolkit';
.session {
  overflow: hidden;

  &__toggle {
    display: block;
    height: 45px;
    width: 100%;
    margin: 10px 0 0;
    padding: 10px;

    background-color: $color-gray;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;

    border-radius: $border-radius;
    border: 2px solid rgba(0,0,0,0);
    color: $text-color;
    cursor: pointer;
    font-weight: bold;
    text-transform: uppercase;

    transition: height 400ms ease;

    .icon-chevron {
      fill: $text-color;
      stroke: $text-color;
    }

    .session__toggle__icon {
      transform: rotate(180deg);
      margin-right: 5px;
    }

    &__contents {
      display:flex;
      align-items: center;
      justify-content: center;

      height: 100%;
      width: 100%;

      background-color: rgba($color-gray, 0.5);
      text-transform: uppercase;
      transition: color 400ms ease;
    }

    &:hover {
      border: 2px solid $color-dark-gray-faded;
    }

    &:focus {
      outline: none !important;
      border: 2px solid $color-dark-gray-faded;
    }
  }

  &__messages {
    display: block;
    position: relative;
    margin: 20px 0;
    padding: 0;
  }

  &--collapsed &__toggle {
    background-size: 0 0;

    &__contents {
      background-color: rgba($color-gray, 0);
      align-items: left;
      justify-content: left;
    }
  }

  &--expanded &__toggle {
    height: 300px;
    padding: 0;
    font-size: 48px;
    font-weight: bold;
    overflow: hidden;
    border: 0;

    .session__toggle__icon {
      transform: rotate(0deg) scale(2);
      margin-right: 20px;
    }
  }

  &--disabled {
    cursor: default;
    .session__toggle {
      &:hover,
      &:focus {
        cursor: default;
        border: 2px solid rgba(0,0,0,0);
      }
    }
  }
}
</style>
