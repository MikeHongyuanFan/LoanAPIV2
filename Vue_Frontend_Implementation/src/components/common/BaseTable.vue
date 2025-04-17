<template>
  <div class="base-table">
    <!-- Table Filter Section -->
    <div class="base-table__filters mb-4" v-if="showFilters">
      <v-row>
        <v-col cols="12" sm="6" md="4" v-if="searchable">
          <v-text-field
            v-model="searchQuery"
            density="comfortable"
            variant="outlined"
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
            @input="handleSearch"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4" v-for="(filter, index) in filters" :key="index">
          <component
            :is="filter.component || 'v-select'"
            v-model="activeFilters[filter.key]"
            :items="filter.options"
            :label="filter.label"
            density="comfortable"
            variant="outlined"
            hide-details
            clearable
            @update:model-value="handleFilterChange"
          ></component>
        </v-col>
        <v-col cols="12" sm="6" md="4" class="d-flex justify-end align-center" v-if="hasActiveFilters">
          <v-btn
            variant="text"
            color="primary"
            @click="clearFilters"
            prepend-icon="mdi-filter-remove"
          >
            Clear Filters
          </v-btn>
        </v-col>
      </v-row>
    </div>

    <!-- Table Actions Section -->
    <div class="base-table__actions d-flex justify-space-between align-center mb-4" v-if="$slots.actions || selectable">
      <div class="base-table__selection-actions" v-if="selectable && selectedItems.length > 0">
        <span class="text-body-1 mr-4">{{ selectedItems.length }} selected</span>
        <slot name="selection-actions" :selected="selectedItems"></slot>
      </div>
      <div class="base-table__custom-actions">
        <slot name="actions"></slot>
      </div>
    </div>

    <!-- Main Table -->
    <v-card>
      <v-data-table
        v-model="selectedItems"
        :headers="headers"
        :items="filteredItems"
        :items-per-page="itemsPerPage"
        :loading="loading"
        :search="searchQuery"
        :sort-by="sortBy"
        :multi-sort="multiSort"
        :item-value="itemValue"
        :show-select="selectable"
        class="base-table__table"
        @update:options="handleOptionsUpdate"
      >
        <!-- Loading -->
        <template v-slot:loading>
          <v-skeleton-loader
            v-for="i in 5"
            :key="i"
            type="table-row"
            class="my-2"
          ></v-skeleton-loader>
        </template>

        <!-- Empty State -->
        <template v-slot:no-data>
          <div class="d-flex flex-column align-center py-8">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-database-off</v-icon>
            <h3 class="text-h6 text-grey-darken-1">{{ noDataText }}</h3>
            <p class="text-body-2 text-grey-darken-1" v-if="hasActiveFilters">
              Try changing your search or filters
            </p>
            <slot name="no-data-actions"></slot>
          </div>
        </template>

        <!-- Custom Headers -->
        <template v-for="header in headers" :key="header.key" v-slot:[`header.${header.key}`]="{ column }">
          <slot :name="`header.${header.key}`" :column="column">
            {{ column.title }}
          </slot>
        </template>

        <!-- Custom Item Slots -->
        <template v-for="header in headers" :key="header.key" v-slot:[`item.${header.key}`]="{ item, column, value }">
          <slot :name="`item.${header.key}`" :item="item" :column="column" :value="value">
            {{ value }}
          </slot>
        </template>

        <!-- Actions Column -->
        <template v-slot:item.actions="{ item }">
          <slot name="item.actions" :item="item">
            <div class="d-flex justify-end">
              <v-btn
                v-for="(action, index) in rowActions"
                :key="index"
                :icon="action.icon"
                :color="action.color || 'default'"
                size="small"
                variant="text"
                @click="action.handler(item)"
                :disabled="action.disabled ? action.disabled(item) : false"
                :title="action.title"
              ></v-btn>
            </div>
          </slot>
        </template>

        <!-- Bottom Slot for Pagination -->
        <template v-slot:bottom>
          <div class="d-flex align-center justify-space-between pa-4">
            <div>
              <span class="text-caption text-grey-darken-1">
                {{ paginationText }}
              </span>
            </div>
            <v-pagination
              v-if="totalItems > itemsPerPage"
              v-model="page"
              :length="Math.ceil(totalItems / itemsPerPage)"
              :total-visible="7"
              @update:model-value="handlePageChange"
            ></v-pagination>
          </div>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

// Props
const props = defineProps({
  // Data
  headers: {
    type: Array,
    required: true
  },
  items: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  itemValue: {
    type: String,
    default: 'id'
  },
  
  // Filtering
  searchable: {
    type: Boolean,
    default: true
  },
  filters: {
    type: Array,
    default: () => []
  },
  showFilters: {
    type: Boolean,
    default: true
  },
  
  // Sorting
  sortBy: {
    type: Array,
    default: () => []
  },
  multiSort: {
    type: Boolean,
    default: false
  },
  
  // Pagination
  itemsPerPage: {
    type: Number,
    default: 10
  },
  totalItems: {
    type: Number,
    default: null
  },
  serverSide: {
    type: Boolean,
    default: false
  },
  
  // Selection
  selectable: {
    type: Boolean,
    default: false
  },
  
  // Row actions
  rowActions: {
    type: Array,
    default: () => []
  },
  
  // Text customization
  noDataText: {
    type: String,
    default: 'No data available'
  }
})

// Emits
const emit = defineEmits([
  'update:options',
  'filter',
  'search',
  'page-change',
  'sort',
  'update:selected'
])

// Reactive state
const searchQuery = ref('')
const activeFilters = ref({})
const selectedItems = ref([])
const page = ref(1)
const options = ref({
  page: 1,
  itemsPerPage: props.itemsPerPage,
  sortBy: props.sortBy
})

// Computed properties
const hasActiveFilters = computed(() => {
  return Object.values(activeFilters.value).some(value => 
    value !== null && value !== undefined && value !== '' && 
    (Array.isArray(value) ? value.length > 0 : true)
  )
})

const filteredItems = computed(() => {
  if (props.serverSide) {
    return props.items
  }
  
  let result = [...props.items]
  
  // Apply filters
  if (hasActiveFilters.value) {
    Object.entries(activeFilters.value).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        if (Array.isArray(value)) {
          if (value.length > 0) {
            result = result.filter(item => value.includes(item[key]))
          }
        } else {
          result = result.filter(item => {
            const itemValue = item[key]
            if (typeof itemValue === 'string') {
              return itemValue.toLowerCase().includes(String(value).toLowerCase())
            }
            return itemValue === value
          })
        }
      }
    })
  }
  
  return result
})

const paginationText = computed(() => {
  const start = (page.value - 1) * props.itemsPerPage + 1
  const end = Math.min(page.value * props.itemsPerPage, props.totalItems || filteredItems.value.length)
  const total = props.totalItems || filteredItems.value.length
  
  return `${start}-${end} of ${total}`
})

// Methods
const handleSearch = () => {
  if (props.serverSide) {
    emit('search', searchQuery.value)
  }
}

const handleFilterChange = () => {
  if (props.serverSide) {
    emit('filter', activeFilters.value)
  }
  // Reset to first page when filters change
  page.value = 1
}

const clearFilters = () => {
  searchQuery.value = ''
  activeFilters.value = {}
  if (props.serverSide) {
    emit('filter', {})
    emit('search', '')
  }
}

const handleOptionsUpdate = (newOptions) => {
  options.value = newOptions
  emit('update:options', newOptions)
  
  if (props.serverSide) {
    if (newOptions.sortBy) {
      emit('sort', newOptions.sortBy)
    }
  }
}

const handlePageChange = (newPage) => {
  emit('page-change', newPage)
}

// Watchers
watch(selectedItems, (newValue) => {
  emit('update:selected', newValue)
})

// Initialize filters
onMounted(() => {
  // Initialize empty filter values
  const initialFilters = {}
  props.filters.forEach(filter => {
    initialFilters[filter.key] = filter.default || null
  })
  activeFilters.value = initialFilters
})
</script>

<style scoped>
.base-table {
  width: 100%;
}

.base-table__table :deep(.v-data-table__tr:hover) {
  background-color: rgba(0, 0, 0, 0.04);
}

.base-table__table :deep(.v-data-table__tr--clickable) {
  cursor: pointer;
}
</style>
