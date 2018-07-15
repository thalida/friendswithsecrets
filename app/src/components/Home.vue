<template>
  <div class="home">
    <Thread
      v-for="(participant, index) in participantOrder"
      :key="index"
      v-bind:participant="participant"
      v-bind:location="'home'"
      v-on:session-select="onSessionSelect" />
  </div>
</template>

<script>
import Thread from './Thread';

export default {
  name: 'Home',
  components: {
    Thread,
  },
  data() {
    return {
      participantOrder: ['akilah', 'robyn', 'timothy'],
    };
  },
  mounted() {
    this.$root.$on('session-select', this.onSessionSelect);
  },
  watch: {
    $route() {},
  },
  methods: {
    onSessionSelect() {},
  },
};
</script>

<style lang="scss" scoped>
.home {
  display: block;
  position: relative;
  width: 80%;
  margin: 0 auto;

  &:after {
      content: "";
      display: table;
      clear: both;
  }
}
</style>
