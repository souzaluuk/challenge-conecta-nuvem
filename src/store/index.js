import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isSignedIn: false,
    loading: true
  },
  mutations: {
    updateIsSignedIn(state, isSignedIn) {
      state.isSignedIn = isSignedIn;
      state.loading = false;
    },
    updateLoading(state, loading) {
      state.loading = loading;
    }
  },
  actions: {
    login({ commit }) {
      commit("updateIsSignedIn", true);
    },
    logout({ commit }) {
      commit("updateIsSignedIn", false);
    },
    setLoading({ commit }, loading) {
      commit("updateLoading", loading);
    }
  },
  modules: {}
});
