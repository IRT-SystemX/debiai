<template>
  <div id="TagCreator">
    <h2>Tag the selected values</h2>
    <form
      v-on:submit.prevent
      class="dataGroup"
    >
      <!-- createdTags -->
      <!-- Selected samples -->
      <div class="data">
        <span class="name"> Selected samples </span>
        <span class="value"> {{ selectedData.length }} / {{ data.nbLines }} </span>
      </div>
      <div class="data">
        <span class="name"> Tag name </span>
        <span class="value">
          <input
            type="text"
            v-model="tagName"
            style="flex: 2"
          />
          <select v-model="tagName">
            <option
              v-for="taggedColName in taggedColumns"
              :key="taggedColName"
            >
              {{ taggedColName }}
            </option>
          </select>
        </span>
      </div>
      <div class="data">
        <span class="name"> Tag value : </span>
        <span class="value">
          <input
            type="number"
            v-model="tagValue"
          />
        </span>
      </div>
    </form>
    <span>
      <button
        type="submit"
        @click="create"
        :disabled="!tagNameOk || !tagValueOk"
      >
        Create the tag
      </button>
      <button
        @click="$emit('cancel')"
        class="red"
      >
        Cancel
      </button>
    </span>
  </div>
</template>

<script>
export default {
  name: "TagCreator",
  data() {
    return {
      tagName: "My tag",
      tagValue: 1,
      taggedColumns: [],
    };
  },
  props: {
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
    // Load the tagged columns name
    this.taggedColumns = this.data.columns.filter((c) => c.category == "tag").map((c) => c.label);
  },
  methods: {
    create() {
      let tagValue = parseInt(this.tagValue);

      // Check if tag already exist
      let column = this.data.columns.find((c) => c.label === this.tagName && c.category === "tag");
      let values;
      if (column) {
        // Update tag values
        values = column.values;
        this.selectedData.forEach((i) => (values[i] = tagValue));
        let uniques = [...new Set(values)].sort((a, b) => a - b);
        column.values = values;
        column.uniques = uniques;
        column.nbOccu = uniques.length;
        column.min = Math.min(...uniques);
        column.max = Math.max(...uniques);
        column.average = values.reduce((a, b) => a + b, 0) / this.data.nbLines || 0;
        this.$store.commit("sendMessage", {
          title: "success",
          msg: "Tag updated successfully",
        });
      } else {
        // Create new tag
        values = new Array(this.data.nbLines).fill(0);
        this.selectedData.forEach((i) => (values[i] = tagValue));
        let uniques = [...new Set(values)].sort((a, b) => a - b);
        let nbOccu = uniques.length;
        this.data.columns.push({
          label: this.tagName,
          index: this.data.nbColumns,
          type: Number,
          typeText: "Num",
          category: "tag",
          values,
          uniques,
          nbOccu,
          min: Math.min(...uniques),
          max: Math.max(...uniques),
          average: values.reduce((a, b) => a + b, 0) / this.data.nbLines || 0,
        });
        this.data.labels.push(this.tagName);
        this.data.nbColumns += 1;
        this.tagCreationWidget = false;
        this.$store.commit("sendMessage", {
          title: "success",
          msg: "Tag created successfully",
        });
        this.$emit("cancel");
      }
    },
  },
  computed: {
    createdTags() {
      return this.data.columns.filter((c) => c.category === "tag").map((c) => c.label);
    },
    tagNameOk() {
      return (
        this.tagName.length >= 1 &&
        !this.data.columns.some((c) => c.label === this.tagName && c.category !== "tag")
      );
    },
    tagValueOk() {
      return this.tagValue !== "";
    },
  },
};
</script>

<style scoped>
.errorMsg {
  color: red;
}

.dataGroup {
  flex-direction: column;
}
.dataGroup .data + .data {
  padding-top: 4px;
}
.dataGroup .value {
  flex: 1;
}
</style>
