# 遍历目录
```java
@Test
void pathTest() throws IOException {
    AtomicInteger directoryCount = new AtomicInteger();
    AtomicInteger fileCount = new AtomicInteger();
    Files.walkFileTree(Paths.get("D:/software_work/jdk-17.0.2"), new SimpleFileVisitor<Path>() {
        @Override
        public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
            directoryCount.incrementAndGet();
            System.out.println("目录：" + dir);
            return super.preVisitDirectory(dir, attrs);
        }

        @Override
        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
            fileCount.incrementAndGet();
            System.out.println("文件：" + file);
            return super.visitFile(file, attrs);
        }
    });
    System.out.println("目录数量：" + directoryCount.get());
    System.out.println("文件数量：" + fileCount.get());
}
```

# 拷贝目录
```java
@Test
void copyDirectory() {
    String source = "D:\\software_work\\apache-maven-3.8.4";
    String target = "D:\\software_work\\apache-maven";
    try {
        Files.walk(Paths.get(source)).forEach(path -> {
            String targetDirectory = path.toString().replace(source, target);
            // 目录
            if (Files.isDirectory(path)) {
                try {
                    Files.createDirectory(Paths.get(targetDirectory));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            // 文件
            else if (Files.isRegularFile(path)) {
                try {
                    Files.copy(path, Paths.get(targetDirectory));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

# 复制文件
```
@Test
void copyFileTest() {
    Path path = Paths.get("./头像.jpg");
    if (!Files.exists(path)) {
        return;
    }
    Path pathNew = Paths.get("./头像2.jpg");
    try {
        //StandardCopyOption.REPLACE_EXISTING 如果文件存在就覆盖
        Files.copy(path, pathNew, StandardCopyOption.REPLACE_EXISTING);
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

# 移动文件
```java
@Test
void moveFileTest() {
    Path path = Paths.get("./头像2.jpg");
    if (!Files.exists(path)) {
        return;
    }
    Path pathNew = Paths.get("D:/头像2.jpg");
    try {
        //StandardCopyOption.REPLACE_EXISTING 如果文件存在就覆盖
        Files.move(path, pathNew, StandardCopyOption.REPLACE_EXISTING);
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```
