//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);  // アドレスを返す
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

// 双方向リスト
typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
  struct my_metadata_t *prev;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap[4];

//
// Helper functions (feel free to add/remove/edit!)
//

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  // assert(!metadata->prev);
  int N = 4;
  int bin[] = {32, 128, 512, 1024};
  bool flag = false;
  for (int i = 0; i < N; i++) {
    if (metadata->size <= bin[i]) {
      my_metadata_t *cur = my_heap[i].free_head;
      // 前から追加するべき場所を探す
      while (cur) {
        if (cur->size > metadata->size) {
          metadata->next = cur;
          metadata->prev = cur->prev;
          cur = metadata;
          flag = true;
        }
        cur = cur->next;
      }
      printf("add to free list\n");
      // 一番最後に追加する場合
      if (!flag) {
        metadata->next = &my_heap[i].dummy;
        my_heap[i].free_head = metadata;
      }
    }
    if (flag) break;
  }
}

my_metadata_t *my_get_free_head(size_t size) {
  int N = 4;
  int bin[] = {32, 128, 512, 1024};
  for (int i = 0; i < N; i++) {
    if (size <= bin[i]) {
      return my_heap[i].free_head;
    }
  }
  return NULL;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  // if (prev) {
  //   prev->next = metadata->next;
  //   metadata->next->prev = prev;
  // } else {
  // 双方向リストの削除
  metadata->prev->next = metadata->next;
  metadata->next->prev = metadata->prev;
  // }
  metadata->next = NULL;
  metadata->prev = NULL;
  printf("free!\n");
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for (int i = 0; i < 5; i++) {
    my_heap[i].free_head = &my_heap[i].dummy;
    my_heap[i].dummy.size = 0;
    my_heap[i].dummy.next = NULL;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  printf("my_malloc(%zu)\n", size);
  my_metadata_t *metadata = my_get_free_head(size);
  my_metadata_t *prev = NULL;
  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_fit_prev = NULL;
  // Best-fit free slot selection
  while (metadata) {
    prev = metadata;
    metadata = metadata->next;
    // Find the best-fit slot: the smallest free slot that is large enough
    if (metadata && metadata->size >= size &&
        (!best_fit || metadata->size < best_fit->size)) {
      best_fit = metadata;
      best_fit_prev = prev;
    }
    if (best_fit) {
      metadata = best_fit;
      prev = best_fit_prev;
    }
    // now, metadata points to the first free slot
    // and prev is the previous entry.

    if (!metadata) {
      // 開いているスロットがない場合はOSに新しいメモリを要求する　
      // There was no free slot available. We need to request a new memory
      // region from the system by calling mmap_from_system().
      //
      //     | metadata | free slot |
      //     ^
      //     metadata
      //     <---------------------->
      //            buffer_size
      size_t buffer_size = 4096;
      my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
      metadata->size = buffer_size - sizeof(my_metadata_t);
      metadata->next = NULL;
      metadata->prev = prev;
      // Add the memory region to the free list.
      my_add_to_free_list(metadata);
      // Now, try my_malloc() again. This should succeed.
      return my_malloc(size);
    }

    // |ptr| is the beginning of the allocated object.
    //
    // ... | metadata | object | ...
    //     ^          ^
    //     metadata   ptr
    void *ptr = metadata + 1;
    size_t remaining_size = metadata->size - size;
    // Remove the free slot from the free list.
    my_remove_from_free_list(metadata, prev);

    if (remaining_size > sizeof(my_metadata_t)) {
      // Shrink the metadata for the allocated object
      // to separate the rest of the region corresponding to remaining_size.
      // If the remaining_size is not large enough to make a new metadata,
      // this code path will not be taken and the region will be managed
      // as a part of the allocated object.
      metadata->size = size;
      // Create a new metadata for the remaining free slot.
      //
      // ... | metadata | object | metadata | free slot | ...
      //     ^          ^        ^
      //     metadata   ptr      new_metadata
      //                 <------><---------------------->
      //                   size       remaining size
      my_metadata_t *new_metadata =
          (my_metadata_t *)((char *)ptr + size);  // size byteb分だけptrをずらす
      new_metadata->size = remaining_size - sizeof(my_metadata_t);
      new_metadata->next = NULL;
      // Add the remaining free slot to the free list.
      my_add_to_free_list(new_metadata);
    }
    return ptr;
  }
}
// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.

void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
