<template>
  <div class="people container-wrapper">
      <span
        v-for="(participant, index) in participantOrder"
        class="person"
        :class="['person--' + participant]"
        :key="index">
        <router-link
          class="person_link"
          :to="{
            name: 'Thread',
            params: {
              participant: participant,
              session: selectedSession,
            },
            query: queryParams
          }"
        >
          {{people[participant].full_name}}
        </router-link>
      </span>
  </div>
</template>

<script>
export default {
  name: 'People',
  computed: {
    queryParams() {
      return this.$store.state.queryParams;
    },
    people() {
      return this.$store.state.people;
    },
    participantOrder() {
      return this.$store.state.participantOrder;
    },
    selectedSession() {
      return this.$store.state.selectedSession;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../assets/styles/toolkit';

.people {
  display: flex;
  position: relative;
  justify-content: space-between;
  z-index: 1;
}

.person {
  margin: 16px 0;
  text-align: center;
  font-weight: bold;
  font-size: 22px;
  color: $color-dark-gray;

  &_link {
    display: block;
    text-decoration: none;
    transition: color 400ms ease;
  }

  @media not all and (hover: none) {
    &:hover {
      animation-duration: 500ms;
      animation-name: bounce;
      animation-fill-mode: backwards;
    }
  }

  @media (min-width: 500px) {
    font-size: 32px;
  }

  @media (min-width: 800px) {
    font-size: 38px;
    &:first-child {
      text-align: left;
    }

    &:last-child {
      text-align: right;
    }
  }
}

.nightmode {
  .person, .person a {
    color: $night-name-color-disabled;
  }
}

// inpsiration: http://www.developerdrive.com/2015/01/8-simple-css-hover-effects/
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-4px);
  }
}

</style>
