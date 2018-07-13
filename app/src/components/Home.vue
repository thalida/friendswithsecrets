<template>
  <div class="home">
    <Header v-bind:location="'home'" />
    <Thread
      v-for="(participant, index) in participantOrder"
      :key="index"
      v-bind:participant="participant"
      v-bind:location="'home'" />
  </div>
</template>

<script>
import Header from './Header';
import Thread from './Thread';

export default {
  name: 'Home',
  components: {
    Header,
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
    &:after {
        content: "";
        display: table;
        clear: both;
    }
}
</style>

