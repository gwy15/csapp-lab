typedef struct Node_s {
    int val;
    Node* left;
    Node* right;
} Node;

int fun7(Node* root, int x) {
    if (root == 0) {
        return -1;
    }
    int val = root->val;
    if (x == val) {
        return 0;
    } else if (val < x) {
        int r = fun7(root->right, x);
        return r + r + 1;
    } else {
        int r = fun7(root->left, x);
        return r + r;
    }
}

/**
 *                root@0x6030f0
 *                  (val:36)
 *             /                 \
 *     addr:0x603110            addr:
 *        val:8                   ___
 *         /    \                /   \ 
 *       ___  addr:0x603150   ___    ___ 
 *               val:22
 * 
 */

