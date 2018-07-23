<template>
  <div id="app">
    <Header />
    <router-view />
  </div>
</template>

<script>
import Header from './Header';

export default {
  name: 'Base',
  components: {
    Header,
  },
  created() {
    this.$session.start();
  },
};
</script>

<style lang="scss">
@import '../assets/styles/colors';
html {
  box-sizing: border-box;
}

*, *:before, *:after {
  box-sizing: inherit;
}

body {
  background-color: $body-bg-color;
  margin: 0;
  padding: 0;
  font: 16px/1.2 'Dosis', sans-serif;
  color: $text-color;
}

a {
  color: $text-color;
}

ol {
  padding: 0;
  margin: 0;
  list-style-type: none;
}

li {
  list-style: none;
}
</style>
