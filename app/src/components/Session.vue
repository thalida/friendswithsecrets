<template>
  <li class="session" :class="[sessionToggleClass]" v-if="hasMessages">
    <transition name="animation-fade">
      <a
        class="session__toggle"
        v-on:click="toggle"
        v-on:keyup.enter="toggle()"
        :title="(isToggleOpen ? 'Close' : 'Open') + ' Session #' + sessionNumber"
        tabindex="0">
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
        <span>{{sessionNumber}}. Session</span>
      </a>
    </transition>
    <transition name="animation-fade-height">
      <div class="session__image"
          v-if="isToggleOpen"
          :style="{ backgroundImage: 'url('+sessionHeader.image_url+')' }">
        <span class="session__header">{{ sessionHeader.title }}</span>
      </div>
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
    display:flex;
    align-items: center;
    justify-content: left;
    flex-direction: row;

    height: 45px;
    width: 100%;
    margin: 10px 0 0;
    padding: 10px;

    background-color: $color-gray;
    border-radius: $border-radius;
    border: 2px solid rgba(0,0,0,0);
    color: $text-color;
    cursor: pointer;
    font-weight: bold;
    text-transform: uppercase;

    transition: color 400ms ease-in-out, border-radius 400ms ease-in-out;

    .icon-chevron {
      fill: $text-color;
      stroke: $text-color;
    }

    &__icon {
      margin-right: 5px;
      transition: transform 400ms ease;
    }

    &:hover {
      border: 2px solid $color-dark-gray-faded;
    }

    &:focus {
      outline: none !important;
      border: 2px solid $color-dark-gray-faded;
    }
  }

  &__image {
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    height: 150px;
    border-radius: 0 0 $border-radius $border-radius;

    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;

    @media (min-width: 500px) {
      height: 225px;
    }

    @media (min-width: 800px) {
      height: 300px;
    }
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    background-color: rgba($color-dark-gray, 0);
    font-size: 30px;
    font-weight: bold;

    transition: background-color 400ms ease;

    @media (min-width: 500px) {
      font-size: 42px;
    }

    @media (min-width: 800px) {
      font-size: 48px;
    }
  }

  &__messages {
    display: block;
    position: relative;
    margin: 20px 0;
    padding: 0;
  }

  &--collapsed &__toggle {
    &__icon {
      transform: rotate(90deg);
    }

    &__contents {
      background-color: rgba($color-gray, 0);
    }
  }

  &--expanded &__toggle {
    border-radius: $border-radius $border-radius 0 0;

    &__icon {
      transform: rotate(0deg);
    }
  }

  &--disabled {
    cursor: default;
    .session__toggle {
      .session__toggle__contents {
        background-color: rgba($color-gray, 0.5);
      }
      &:hover,
      &:focus {
        cursor: default;
        border: 2px solid rgba(0,0,0,0);
      }
    }
  }
}
</style>
