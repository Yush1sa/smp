<script setup>

import useProfileStore from "@/stores/profileStore.js";
import {storeToRefs} from "pinia";

const profileStore = useProfileStore();
const {
    isAuthenticated,
    userName
} = storeToRefs(profileStore)

async function onLogoutButtonClick() {
    profileStore.logout()
}



</script>

<template>
  <nav class="navbar navbar-expand-sm bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse w-100 justify-content-between" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/admin">Admin</a>
          </li>
        </ul>
        <form role="search">
              Авторизован: {{ userName }}
          <button v-if="isAuthenticated" class="btn btn-outline-success" type="submit" @click="onLogoutButtonClick()">
              Выйти
          </button>
        </form>
      </div>
    </div>
  </nav>
</template>

<style scoped>

</style>