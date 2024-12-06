<script>
export default {
  name: "FullscreenDialogPage",
  props: {
    fullWidth: {
      type: Boolean,
      default: false,
    },
    dialogOnInitialRoute: {
      type: Boolean,
      default: false,
    },
    fallbackUrl: {
      type: [Object, String],
      default: null,
    },
  },
  methods: {
    handleClose() {
      this.$backOrElse(this.fallbackUrl);
    },
  },
  computed: {
    isDialog() {
      return (
        this.dialogOnInitialRoute ||
        this.$route.path !== this.$router.history._startLocation
      );
    },
    component() {
      return this.isDialog ? "v-dialog" : "v-sheet";
    },
  },
};
</script>

<template>
  <component
    :is="component"
    :value="true"
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
    v-bind="$attrs"
    v-on="$listeners"
  >
    <v-card elevation="0">
      <v-toolbar v-if="isDialog">
        <slot name="cancel">
          <v-btn icon @click="handleClose">
            <v-icon>$cancel</v-icon>
          </v-btn>
        </slot>

        <v-toolbar-title>
          {{ $root.toolbarTitle }}
        </v-toolbar-title>

        <v-spacer></v-spacer>

        <v-toolbar-items>
          <slot name="actions" :toolbar="true" />
        </v-toolbar-items>
      </v-toolbar>

      <div
        :class="{
          'main-container': isDialog,
          'pa-3': isDialog,
          'full-width': isDialog && ($route.meta.fullWidth ?? fullWidth),
        }"
      >
        <slot />
        <slot name="actions" v-if="!isDialog" :toolbar="false" />
      </div>
    </v-card>
  </component>
</template>
