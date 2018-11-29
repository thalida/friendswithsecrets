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
          <img
            class="name-image name-image--still"
            :src="people[participant].img_urls.still"
            :alt="people[participant].full_name" />
          <img
            class="name-image name-image--moving"
            :src="people[participant].img_urls.moving"
            :alt="people[participant].full_name" />
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
    position: relative;
    text-decoration: none;
    transition: color 400ms ease;
  }

  .name-image {
    display: block;
    position: relative;
    width: 100%;

    &--still {
      display: block;
    }

    &--moving {
      display: none;
    }
  }

  @media not all and (hover: none) {
    &:hover {
      .name-image--still {
        display: none;
      }

      .name-image--moving {
        display: block;
      }
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

@media screen and (max-width: 800px), screen and (max-height: 400px) {
  .people {
    width: calc(95% - 110px);
    margin: 0 auto 0 5%;
    justify-content: left;
  }

  .person {
    margin: 16px 5px;
  }

  .person .name-image {
    width: 120%;
  }
}

@media screen and (max-width: 330px), screen and (max-height: 400px) {
  .person .name-image {
    width: 130%;
  }
}

.nightmode {
  .person, .person a {
    color: $night-color-medium;
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
