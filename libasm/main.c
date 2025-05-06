#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "libasm.h"

#define RUN_TEST(desc, expr)                                             \
    do {                                                                 \
        int ok = (expr) ? 1 : 0;                                         \
        printf("%-45s : %s\n", desc, ok ? "✅ OK" : "❌ FAIL");           \
    } while (0)

#define RUN_TEST_ERR(desc, expr)                                         \
    do {                                                                 \
        int ok = (expr) ? 1 : 0;                                         \
        printf("%-45s : %s (errno=%d: %s)\n",                            \
               desc, ok ? "✅ OK" : "❌ FAIL", errno, strerror(errno));   \
    } while (0)

/* --------------------------------------------------
 * Test of ft_strlen
 * -------------------------------------------------- */
void test_strlen(void) {
    printf("\n=== ft_strlen ===\n");
    const char *tests[] = {
        "", "a", "hello", "hello world!", "1234567890",
        "with spaces", "\t\n\r", "😃😄😁", NULL
    };
    for (int i = 0; tests[i]; i++) {
        size_t ft = ft_strlen(tests[i]);
        size_t std = strlen(tests[i]);
        RUN_TEST("original strlen  vs ft_strlen", ft == std);
    }
    // very long string
    char *long_str = malloc(10001);
    if (long_str) {
        memset(long_str, 'x', 10000);
        long_str[10000] = '\0';
        RUN_TEST("ft_strlen on 10000 'x'", ft_strlen(long_str) == 10000);
        free(long_str);
    }
}

/* --------------------------------------------------
 * Test of ft_strcpy
 * -------------------------------------------------- */
void test_strcpy(void) {
    printf("\n=== ft_strcpy ===\n");
    char dst1[32], dst2[32];
    const char *tests[] = {
        "", "abc", "42", "test copy", "😀 utf8", NULL
    };
    for (int i = 0; tests[i]; i++) {
        memset(dst1, 0, sizeof(dst1));
        memset(dst2, 0, sizeof(dst2));
        char *rft = ft_strcpy(dst1, tests[i]);
        char *rst = strcpy(dst2, tests[i]);
        RUN_TEST("simple strcpy", strcmp(rft, rst) == 0);
    }
    // Self-copy (src == dst)
    {
        char self[16] = "hello";
        RUN_TEST("ft_strcpy self-copy",
                 ft_strcpy(self, self) == self && strcmp(self, "hello") == 0);
    }
#ifdef TEST_NULL
    RUN_TEST("ft_strcpy dst=NULL", ft_strcpy(NULL, "test") == NULL);
    RUN_TEST("ft_strcpy src=NULL", ft_strcpy(dst1, NULL) == NULL);
#endif
}

/* --------------------------------------------------
 * Test of ft_strcmp
 * -------------------------------------------------- */
void test_strcmp(void) {
    printf("\n=== ft_strcmp ===\n");
    struct { const char *a, *b; } tests[] = {
        { "", "" },
        { "a", "a" },
        { "a", "b" },
        { "abc", "abd" },
        { "abc", "abc" },
        { "abc", "ab" },
        { NULL, NULL }
    };
    for (int i = 0; tests[i].a; i++) {
        int ft = ft_strcmp(tests[i].a, tests[i].b);
        int std = strcmp(tests[i].a, tests[i].b);
        int sft = (ft > 0) - (ft < 0);
        int sstd = (std > 0) - (std < 0);
        RUN_TEST("signed strcmp", sft == sstd);
    }
    // Long strings with mismatch near end
    {
        char a[1001], b[1001];
        memset(a, 'a', 1000); a[1000] = '\0';
        memcpy(b, a, 1001);
        b[999] = 'b';
        RUN_TEST("ft_strcmp long mismatch", ft_strcmp(a, b) < 0);
    }
#ifdef TEST_NULL
    RUN_TEST("ft_strcmp NULL,NULL", ft_strcmp(NULL, NULL) == 0);
    RUN_TEST("ft_strcmp NULL,a", ft_strcmp(NULL, "a") < 0);
    RUN_TEST("ft_strcmp a,NULL", ft_strcmp("a", NULL) > 0);
#endif
}

/* --------------------------------------------------
 * Test de ft_write
 * -------------------------------------------------- */
void test_write(void) {
    printf("\n=== ft_write ===\n");
    ssize_t ret;
    // 1) valid write on stdout
    errno = 0;
    ret = ft_write(1, "Hello from ft_write!\n", 22);
    RUN_TEST("ft_write stdout", ret == 22);
    // 2) count = 0
    errno = 0;
    ret = ft_write(1, "data", 0);
    RUN_TEST("ft_write zero length", ret == 0);
    // 3) buf = NULL, count > 0 -> EFAULT
    errno = 0;
    ret = ft_write(1, NULL, 5);
    RUN_TEST_ERR("ft_write NULL buf", ret == -1);
    // 4) mauvais fd
    errno = 0;
    ret = ft_write(-1, "fail", 4);
    RUN_TEST_ERR("ft_write bad fd", ret == -1);
    // 5) writing to a temp file
    {
        char tmpw[] = "./libasm_write_XXXXXX";
        int fd = mkstemp(tmpw);
        if (fd >= 0) {
            const char msg[] = "FileMsg";
            size_t mlen = strlen(msg);
            ret = ft_write(fd, msg, mlen);
            RUN_TEST("ft_write temp file count", ret == (ssize_t)mlen);
            lseek(fd, 0, SEEK_SET);
            char buf[32] = {0};
            read(fd, buf, mlen);
            RUN_TEST("ft_write temp file content", strcmp(buf, msg) == 0);
            close(fd);
            unlink(tmpw);
        } else {
            RUN_TEST("ft_write temp file open", 0);
        }
    }
    // 6) writing to /dev/null
    {
        int dn = open("/dev/null", O_WRONLY);
        if (dn >= 0) {
            errno = 0;
            ret = ft_write(dn, "ignore", 6);
            RUN_TEST("ft_write /dev/null", ret == 6);
            close(dn);
        } else {
            RUN_TEST("open /dev/null", 0);
        }
    }
}

/* --------------------------------------------------
 * Test of ft_read
 * -------------------------------------------------- */
void test_read(void) {
    printf("\n=== ft_read ===\n");
    char buf[32];
    ssize_t ret;
    // 1) read from a small file
    {
        char tmp[] = "./libasm_read_XXXXXX";
        int fd = mkstemp(tmp);
        if (fd >= 0) {
            write(fd, "LibAsmTest", 10);
            lseek(fd, 0, SEEK_SET);
            ret = ft_read(fd, buf, sizeof(buf) - 1);
            if (ret > 0) buf[ret] = '\0';
            RUN_TEST("ft_read small file", ret == 10 && strcmp(buf, "LibAsmTest") == 0);
            close(fd);
            unlink(tmp);
        } else {
            RUN_TEST("ft_read small file open", 0);
        }
    }
    // 2) count = 0 on /dev/null
    {
        int dn = open("/dev/null", O_RDONLY);
        if (dn >= 0) {
            errno = 0;
            ret = ft_read(dn, buf, 0);
            RUN_TEST("ft_read zero length", ret == 0);
            close(dn);
        } else {
            RUN_TEST("open /dev/null for read", 0);
        }
    }
    // 3) buf = NULL, count > 0 -> EFAULT
    errno = 0;
    ret = ft_read(0, NULL, 5);
    RUN_TEST_ERR("ft_read NULL buf", ret == -1);
    // 4) bad fd
    errno = 0;
    ret = ft_read(-1, buf, 5);
    RUN_TEST_ERR("ft_read bad fd", ret == -1);
    // 5) reading from multiple chunks of a file
    {
        char tmp2[] = "./libasm_read2_XXXXXX";
        int fd2 = mkstemp(tmp2);
        if (fd2 >= 0) {
            size_t total = 1000;
            char *big = malloc(total);
            for (size_t i = 0; i < total; i++) big[i] = 'A' + (i % 26);
            write(fd2, big, total);
            lseek(fd2, 0, SEEK_SET);
            size_t read_total = 0;
            while ((ret = ft_read(fd2, buf, 10)) > 0) {
                read_total += ret;
            }
            RUN_TEST("ft_read in chunks total", read_total == total);
            free(big);
            close(fd2);
            unlink(tmp2);
        } else {
            RUN_TEST("ft_read big file open", 0);
        }
    }
}

/* --------------------------------------------------
 * Test of ft_strdup
 * -------------------------------------------------- */
void test_strdup(void) {
    printf("\n=== ft_strdup ===\n");
    const char *tests[] = { "", "42", "Libasm is fun", NULL };
    for (int i = 0; tests[i]; i++) {
        char *dft = ft_strdup(tests[i]);
        char *dst = strdup(tests[i]);
        RUN_TEST("strdup simple", dft && dst && strcmp(dft, dst) == 0);
        free(dft);
        free(dst);
    }
    // check if the pointer is different
    {
        const char *src = "alias?";
        char *dup = ft_strdup(src);
        RUN_TEST("ft_strdup new alloc", dup && dup != src);
        free(dup);
    }
    // very long string
    {
        char *big = malloc(5001);
        memset(big, 'L', 5000);
        big[5000] = '\0';
        char *dup2 = ft_strdup(big);
        RUN_TEST("ft_strdup long", dup2 && ft_strlen(dup2) == 5000);
        free(dup2);
        free(big);
    }
#ifdef TEST_NULL
    char *dn = ft_strdup(NULL);
    RUN_TEST("ft_strdup NULL", dn == NULL);
#endif
}

/* --------------------------------------------------
 * main
 * -------------------------------------------------- */
int main(void) {
    test_strlen();
    test_strcpy();
    test_strcmp();
    test_write();
    test_read();
    test_strdup();
    return 0;
}
/* --------------------------------------------------
 * end of main.c
 * -------------------------------------------------- */