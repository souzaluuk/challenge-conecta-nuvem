import Vue from "vue";
import VueGapi from "vue-gapi";

Vue.use(VueGapi, {
  apiKey: process.env.VUE_APP_API_KEY,
  clientId: process.env.VUE_APP_CLIENT_ID,
  discoveryDocs: [
    "https://www.googleapis.com/discovery/v1/apis/people/v1/rest"
  ],
  scope: "https://www.googleapis.com/auth/contacts.readonly"
});
