<template>
  <div
    id="modal"
    @click.stop="outsideClick"
  >
    <div id="Panel">
      <slot />
    </div>

    <div id="errors">
      <div
        v-for="(error, index) in errorMessages"
        :key="index"
      >
        <transition name="fade">
          <div
            class="error"
            v-if="error"
          >
            {{ error }}
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Modal",
  props: {
    errorMessages: { type: Array, default: () => [] },
  },
  mounted() {
    // When the modal is opened, we want to disable scrolling on the body
    const bodyOverflowStyle = document.body.style.overflow;
    if (bodyOverflowStyle !== "hidden") {
      document.body.style.overflow = "hidden";
      this.preventBodyScroll = true;
      // The preventBodyScroll variable is used in the beforeDestroy hook
      // Usefull in case of recursive modals
      // (the beforeDestroy would be called before the last modal is closed)
    }
  },
  methods: {
    outsideClick(e) {
      if (e.target.id === "modal") this.$emit("close");
    },
  },
  beforeDestroy() {
    // When the modal is closed, we want to enable scrolling on the body
    if (this.preventBodyScroll) document.body.style.overflow = "auto";
  },
};
</script>

<style>
#modal {
  z-index: 5;
  position: fixed;
  height: 100vh;
  width: 100vw;
  left: 0%;
  top: 0%;
  background-color: rgba(0, 0, 0, 0.5);

  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  backdrop-filter: blur(1px);

  animation: fadeIn 0.1s;
}
#modal:hover {
  cursor: pointer;
}

#Panel {
  max-height: 90vh;
  max-width: 90vw;
  padding: 3vh;
  background-color: rgb(250, 250, 250);
  border-radius: 1vh;
  overflow: auto;
}

#Panel:hover {
  cursor: default;
}

#errors {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#errors .error {
  font-weight: bold;
  border-radius: 10px;
  padding: 5px;
  margin: 10px;
}
</style>
