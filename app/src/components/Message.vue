<template>
  <div class="message" :class="[messageClass]">
    <span class="message__sender">{{message.sender}}</span>
    <p class="message__text">{{message.message}}</p>
  </div>
</template>

<script>
export default {
  name: 'Message',
  props: {
    message: Object,
  },
  data() {
    return {};
  },
  computed: {
    messageClass() {
      return '';
    },
  },
};
</script>

<style lang="scss">
.message {
  &__text {
    display: block;
    position: relative;
    margin: 0;
    padding: 0;
    border-radius: 8px 8px 8px 0px;
  }
}
</style>
