<template>
  <div class="home">
    <Thread
      v-for="(participant, index) in participantOrder"
      :key="index"
      v-bind:participant="participant"
      v-bind:location="'home'" />
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
  created() {},
  methods: {},
};
</script>

<style lang="scss" scoped>
.home {
  width: 80%;
  margin: 0 auto;
  &:after {
      content: "";
      display: table;
      clear: both;
  }
}
</style>
