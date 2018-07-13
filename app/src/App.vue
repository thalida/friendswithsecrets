<template>
  <div id="app">
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {},
};
</script>

<style>
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
  color: #222222;
}

a {
  color: #222222;
}
</style>
