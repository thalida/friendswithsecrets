<template>
  <li class="message" :class="[messageIndexClass, messageSenderClass, messageTypeClass]">
    <div class="message__sender">{{sender.full_name}}</div>
    <p
      v-for="(message, index) in messages" class="message__text"
      :key="index">
      {{message}}
    </p>
  </li>
</template>

<script>
export default {
  name: 'Message',
  props: {
    index: Number,
    messages: Array,
    sender: Object,
  },
  data() {
    return {};
  },
  computed: {
    messageTypeClass() {
      return (this.sender.is_therapist) ? 'message--therapist' : 'message--participant';
    },
    messageSenderClass() {
      return `message--${this.sender.name}`;
    },
    messageIndexClass() {
      return `message--${this.index}`;
    },
  },
};
</script>

<style lang="scss">
@import '../assets/styles/colors';
.message {
  &__sender {
    margin: 15px 0px 5px;

    color: $text-color;
    font-size: 14px;
    font-weight: bold;
    text-transform: lowercase;
  }

  &__text {
    display: block;
    position: relative;
    margin: 5px 0 0;
    padding: 8px;
    border-radius: 8px;
    font-weight: normal;
    background-color: $color-gray;

    &:first-of-type {
      border-radius: 8px 8px 8px 0px;
    }
  }

  &--0 &__sender {
    margin-top: 0;
  }

  &--participant {
    .message__text {
      background-color: $color-participant;
    }
  }
}
</style>
