<template>
  <div class="session">
    Session #{{ index + 1 }}
    <div class="session__messages">
      <Message
        v-for="(message, index) in messages"
        :key="index"
        v-bind:message="message"
        v-bind:sender="sender" />
    </div>
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
    person: Object,
    messages: Array,
  },
  data() {
    return {};
  },
};
</script>

<style lang="scss">
$color: #000;
.sesssion {
}
</style>
