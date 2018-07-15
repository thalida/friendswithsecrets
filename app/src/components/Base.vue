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
  background-color: #FFFFFF;
  margin: 0;
  padding: 0;
  font: 16px/1.2 'Dosis', sans-serif;
  color: $text-color;
}

a {
  color: $text-color;
}
</style>
