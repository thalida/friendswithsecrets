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
          <svg class="session__toggle__icon"
            width="16px" height="10px"
            viewBox="0 0 18 12" version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink">
            <g
              stroke="none"
              stroke-width="1"
              fill="none"
              fill-rule="evenodd"
              stroke-linecap="round"
              stroke-linejoin="round">
                <g stroke="#222222" stroke-width="3">
                  <polyline
                    transform="
                      translate(9.000000, 6.000000)
                      rotate(-180.000000)
                      translate(-9.000000, -6.000000)"
                    points="16 2 9 10 2 2.21177316">
                  </polyline>
                </g>
            </g>
          </svg>
          <span>{{ sessionToggleText }}</span>
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
      return (this.isToggleOpen) ? `${this.sessionHeader.title}` : `${this.sessionNumber}. Session`;
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

    &__icon {
      margin-right: 5px;
      transition: transform 500ms ease;
    }

    &__contents {
      display:flex;
      align-items: center;
      justify-content: center;
      flex-direction: row;

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

    &__icon {
      transform: rotate(90deg);
    }

    &__contents {
      justify-content: left;
      background-color: rgba($color-gray, 0);
    }
  }

  &--expanded &__toggle {
    height: 150px;
    padding: 0;
    font-size: 30px;
    font-weight: bold;
    overflow: hidden;
    border: 0;

    &__icon {
      transform: rotate(0deg) scale(1.5);
      margin-right: 15px;
    }

    @media (min-width: 500px) {
      height: 225px;
      font-size: 42px;

      &__icon {
        transform: rotate(0deg) scale(2);
        margin-right: 20px;
      }
    }

    @media (min-width: 800px) {
      height: 300px;
      font-size: 48px;
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
