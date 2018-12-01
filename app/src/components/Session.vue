<template>
  <li class="session" :class="[sessionToggleClass]" v-if="hasMessages">
    <a
      class="session__toggle"
      v-on:click="toggle"
      v-on:keyup.enter="toggle()"
      :title="sessionAltText">
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
      <span
        class="session__title"
        v-if="sessionTitle.length > 0">
          {{sessionTitle}}
      </span>
      <span class="session__number" v-if="isToggleOpen">{{leftPadSessionNumber}}.</span>
    </a>
    <transition name="animation--fade-height">
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
    <span class="session__toggle">
      <span class="session__title" v-if="sessionTitle.length > 0">
          {{sessionTitle}}
      </span>
      <span class="session__title" v-else></span>
      <span class="session__number">Day {{sessionNumber}}.</span>
    </span>
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
    session: Object,
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
    people() {
      return this.$store.state.people;
    },
    sessionNumber() {
      return this.index + 1;
    },
    leftPadSessionNumber() {
      const pad = (this.sessionNumber < 10) ? '0' : '';
      return `${pad}${this.sessionNumber}`;
    },
    sessionTitle() {
      return (this.session) ? this.session.title : '';
    },
    sessionToggleClass() {
      const toggleClass = this.isToggleOpen ? this.toggleClasses.open : this.toggleClasses.closed;
      return `session--${toggleClass}`;
    },
    sessionAltText() {
      const openStateText = (this.isToggleOpen ? 'Close' : 'Open');
      return `${openStateText} day ${this.sessionNumber}`;
    },
    hasMessages() {
      return typeof this.session !== 'undefined'
            && this.session !== null
            && this.session.messages.length > 0;
    },
    messagesFormatted() {
      const messagesFormatted = [];

      if (!this.hasMessages) {
        return [];
      }

      this.session.messages.forEach((message) => {
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
    position: relative;
    display: flex;
    align-items: center;
    flex-direction: row;

    width: 100%;
    margin: 10px 0 0;
    padding: 14px 16px;

    background-color: $color-gray;
    border-radius: $border-radius;
    border: 2px solid rgba(0,0,0,0);
    color: $text-color;
    cursor: pointer;

    font-size: 20px;
    font-weight: bold;

    .icon-chevron {
      stroke: $text-color;
    }

    &__icon {
      margin-right: 5px;
      transition: transform 400ms ease;
    }

    @media (max-width: 800px) {
      font-size: 16px;
    }
  }

  &__title {
    position: relative;
    left: 0;
    transition: all 300ms;
  }

  &__number {
    text-transform: uppercase;
  }

  &__messages {
    display: block;
    position: relative;
    margin: 20px 0;
    padding: 0;
  }

  &--collapsed {
    .session__toggle {
      justify-content: left;
      &__icon {
        transform: rotate(90deg);
      }
      &__contents {
        background-color: rgba($color-gray, 0);
      }
    }
  }

  &--expanded {
    .session__title {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
    }
    .session__toggle {
      color: $text-color-light;
      justify-content: space-between;
      .icon-chevron {
        stroke: $text-color-light;
      }
      &__icon {
        transform: rotate(180deg);
      }
    }
  }

  &--disabled {
    cursor: default;
    .session__number {
      text-transform: none;
    }
    .session__toggle {
      justify-content: space-between;
      opacity: 0.5;

      &:hover,
      &:focus {
        cursor: default;
        border: 2px solid rgba(0,0,0,0);
      }
    }
  }
}
</style>
