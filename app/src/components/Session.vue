<template>
  <li class="session" :class="[sessionToggleClass]" v-if="hasMessages">
    <transition name="animation-fade">
      <a
        class="session__toggle"
        v-on:click="toggle"
        v-on:keyup.enter="toggle()"
        :title="(isToggleOpen ? 'Close' : 'Open') + ' Session #' + sessionNumber">
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
              <g class="icon-chevron" stroke="#222222" stroke-width="3">
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
        <span class="session__title" v-if="isToggleOpen">{{sessionHeader.title}}</span>
        <span class="text--uppercase">{{sessionToggleText}}</span>
      </a>
    </transition>
    <transition name="animation--fade-height--2x">
    <ol class="session__messages" v-if="isToggleOpen">
      <Message
        v-for="(groupedMessages, index) in messagesFormatted"
        :key="index"
        v-bind:index="index"
        v-bind:messages="groupedMessages.messages"
        v-bind:sender="people[groupedMessages.sender]" />
    </ol>
    </transition>
  </li>
  <li class="session session--disabled" v-else>
    <span class="session__toggle text--uppercase">{{ sessionNumber }}. Session</span>
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
    sessionToggleText() {
      return this.isToggleOpen ? `${this.sessionNumber}.` : `${this.sessionNumber}. Session`;
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

    .icon-chevron {
      stroke: $text-color;
    }

    &__icon {
      margin-right: 5px;
      transition: transform 400ms ease;
    }
  }

  &__title {

  }

  &__messages {
    display: block;
    position: relative;
    margin: 20px 0;
    padding: 0;
  }

  &--collapsed &__toggle {
    &__icon {
      transform: rotate(0deg);
    }

    &__contents {
      background-color: rgba($color-gray, 0);
    }
  }

  &--expanded &__toggle {
    justify-content: space-between;
    color: $text-color-light;

    .icon-chevron {
      stroke: $text-color-light;
    }

    &__icon {
      transform: rotate(90deg);
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
