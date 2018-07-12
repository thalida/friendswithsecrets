<template>
  <section class="thread" :class="[personClass]">
    {{ person.full_name }}
    <Session
      v-for="(messages, index) in sessions"
      :key="index"
      v-bind:index="index"
      v-bind:person="person"
      v-bind:messages="messages" />
  </section>
</template>

<script>
import axios from 'axios';
import Session from './Session';

export default {
  name: 'Thread',
  components: {
    Session,
  },
  props: {
    person: Object,
  },
  data() {
    return {
      sessions: [],
    };
  },
  created() {
    this.getMessages();
  },
  computed: {
    personClass() {
      return `thread--${this.person.name}`;
    },
  },
  methods: {
    getMessages() {
      const prefix = (process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '';
      const path = `${prefix}/api/thread/${this.person.name}`;
      axios.get(path)
        .then((response) => {
          this.sessions = response.data;
        });
    },
  },
};
</script>

<style lang="scss">
.thread {
  &--akilah .message__text {
    background-color: #40DCFB;
  }
  &--robyn .message__text {
    background: #65FFF6;
  }
  &--timothy .message__text {
    background: #18E5EA;
  }
}
</style>
