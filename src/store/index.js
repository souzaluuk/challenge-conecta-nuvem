import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    loading: true,
    user: null
  },
  getters: {
    isSignedIn: ({ user }) => !!user
  },
  mutations: {
    setLoading(state, loading) {
      state.loading = loading;
    },
    setUser(state, user) {
      state.user = user;
    }
  },
  actions: {
    login({ commit }, user) {
      commit("setUser", user);
    },
    logout({ commit }) {
      commit("setUser", null);
    },
    setLoading({ commit }, loading) {
      commit("setLoading", loading);
    }
  },
  modules: {}
});
