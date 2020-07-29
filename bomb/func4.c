int func4(int x, int y, int z) {
    int t = z - y;
    if (y > z) t++;
    t = t >> 1;
    t = t + y;

    // t ~= (y+z) / 2;

    if (t == x) {
        return 0;
    } else if (t < x) {
        return 2 * func4(x, t + 1, z) + 1;
    } else {
        return 2 * func4(x, y, t - 1);
    }
}