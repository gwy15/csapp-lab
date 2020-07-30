typedef struct LinkedListS {
    int val;
    struct LinkedList* next;
} LinkedList;
LinkedList head, tail;


int c_40116f_4011a9() { 
    int rcx, rax;
    LinkedList* ptr;
    int *arr;

    int rsi = 0;
    do {
        rcx = arr[rsi];
        if (arr[rsi] <= 1) {
            ptr = &head;
        } else {
            ptr = &head;
            rax = 1;
            do {
                ptr = ptr -> next;
                rax ++;
            } while (rax != rcx);
        }
        arr[32 + 2*rsi] = ptr;
        rsi += 4;
    } while (rsi != 24);
}

int c_40116f_4011a9_formatted() {
    LinkedList* ptr;
    int *arr;

    for (int i=0; i<24; i+=4) {
        if (arr[i] == 1) {
            ptr = &head;
        } else {
            ptr = &head;
            for (int j=0; j<arr[i]; j++) {
                ptr = ptr -> next;
            }
        }
        arr[32 + 2*i] = ptr;
    }
}

// 将链表连起来
int c_4011ab_4011d9() {
    LinkedList* ptrs[6];

    LinkedList* ptr0 = ptrs[0];
    LinkedList** rax = &ptrs[1];
    LinkedList** ptrs_end = &ptrs[6];
    
    LinkedList* ptr = ptr0;
    do {
        LinkedList* next = *rax;    // next
        ptr->next = *rax;           //
        rax += 8; // next pointer
        if (rax == ptrs_end) {
            break;
        }
        ptr = next;
    } while (1);
    ptr->next = 0;
}


int c_4011da_4011f7() {
    LinkedList* ptrs[6];
    LinkedList* rbx = ptrs[0];
    for (int i=0; i<5; i++) {
        LinkedList* rax = rbx->next;
        int rax = rax->val;
        if (rbx->val < rax) {
            // boom!
        }
        rbx = rbx->next;
    }
}