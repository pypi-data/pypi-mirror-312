<template>
  <v-btn v-bind="{ ...$props, ...$attrs }" v-on="$listeners" icon large>
    <v-icon>$close</v-icon>
  </v-btn>
</template>

<script>
export default {
  name: "DialogCloseButton",
  inheritAttrs: true,
  extends: "v-btn",
};
</script>
