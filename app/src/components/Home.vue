<template>
  <div class="home">
    <Thread
      v-for="(person, index) in peopleOrder"
      :key="index"
      v-if="people[person].is_therapist === false"
      v-bind:person="people[person]" />
  </div>
</template>

<script>
import axios from 'axios';
import Thread from './Thread';

export default {
  name: 'Home',
  components: {
    Thread,
  },
  data() {
    return {
      peopleOrder: ['akilah', 'robyn', 'timothy'],
      people: [],
    };
  },
  created() {
    this.getPeople();
  },
  methods: {
    getPeople() {
      const prefix = (process.env.NODE_ENV === 'development') ? 'http://127.0.0.1:5000' : '';
      const path = `${prefix}/api/people`;
      axios.get(path)
        .then((response) => {
          this.people = response.data;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.home {
    .thread {
        width: 30%;
        margin: 0 1.5%;
        float: left;
    }

    &:after {
        content: "";
        clear: both;
    }
}
</style>

