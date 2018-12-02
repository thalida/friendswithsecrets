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
  width: calc(100% - 70px - 30px);
  margin-top: 50px;
  padding-bottom: 15px;
}

.person {
  text-align: center;
  padding: 0 30px;

  &_link {
    display: block;
    position: relative;
    text-decoration: none;
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
}

@media screen and (max-width: 800px), screen and (max-height: 400px) {
  .people {
    margin-top: 18px;
    padding: 0 5px;
  }

  .person {
    padding: 0;
  }
}

</style>
