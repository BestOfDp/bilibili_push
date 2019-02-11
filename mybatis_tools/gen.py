import os


class Config:
    rootPath = 'E:/Java/spingboot/IntelligentRoom/'
    entity = "domain"
    dao = "dao"
    mapper = "mapper"
    mybatis_xml_path = rootPath + "src/main/resources/mybatis-generator.xml"
    page_helper = "import cn.lsu.chicken.room.helper.PageHelper"
    page = "page"
    size = "size"
    offset = "offset"


class MybatisGen:

    def gen(self):
        config = self._read_file_to_str(Config.mybatis_xml_path)
        self._set_variable(config, "entity", "javaModelGenerator")
        self._set_variable(config, "dao", "javaClientGenerator")
        self._set_variable(config, "mapper", "sqlMapGenerator")

        self._add_annotation_lombok()
        self._add_annotation_component()
        self._add_mapper_xml()

    # lombok模块
    def _annotation_data(self, path):
        content = self._read_file_to_str(path)
        data = "import lombok.Data;\n\n@Data\n"
        index = content.find(str(data.split(";")[0]))
        if index == -1:
            public_index = content.find("public")
            content = content[:public_index] + data + content[public_index:]
            self._write_str_to_file(path, content)

    def _extend_page_helper(self, path):
        content = self._read_file_to_str(path)
        data = Config.page_helper + ";\n\n"
        index = content.find(str(data.split(";")[0]))
        if index == -1:
            public_index = content.find("public")
            content = content[:public_index] + data + content[public_index:]

            # 继承
            extend_index = content.find("Example") + len("Example")
            content = content[:extend_index] + " extends " + Config.page_helper.split(".")[-1] + content[extend_index:]

            # 构造方法
            class_name = path.split("/")[-1].split('.')[0]
            init_index = content.find(class_name)
            add_index = content.find("}", init_index) + 1
            total = '\n\n    public ' + class_name + '(Integer page, Integer size) {\n' \
                                                     '        super(page, size);\n' \
                                                     '        oredCriteria = new ArrayList<Criteria>();\n' \
                                                     '    }'
            content = content[:add_index] + total + content[add_index:]
            self._write_str_to_file(path, content)
            # print(content)

    def _add_annotation_lombok(self):
        file_path = Config.rootPath + Config.entity
        list = os.listdir(file_path)
        for i in list:
            if not i.split(".")[0].endswith("Example"):
                self._annotation_data(file_path + "/" + i)
            else:
                self._extend_page_helper(file_path + "/" + i)

        print("添加Data注解成功！")

    def _add_annotation_component(self):
        file_path = Config.rootPath + Config.dao
        list = os.listdir(file_path)
        for i in list:
            self._add_annotation_component_at(file_path + "/" + i)
            break

        print("添加Component注解成功！")

    def _add_annotation_component_at(self, path):
        content = self._read_file_to_str(path)
        data = "import org.springframework.stereotype.Component;\n\n@Component\n"
        index = content.find(str(data.split(";")[0]))
        if index == -1:
            public_index = content.find("public")
            content = content[:public_index] + data + content[public_index:]
            self._write_str_to_file(path, content)

    def _add_mapper_xml(self):
        file_path = Config.rootPath + Config.mapper
        list = os.listdir(file_path)
        for i in list:
            self._add_mapper_xml_page(file_path + "/" + i)

        print("添加ExamplePage成功！")

    def _add_mapper_xml_page(self, path):
        content = self._read_file_to_str(path)
        data = '\n        ' \
               '<if test="' + Config.page \
               + ' != null and ' \
               + Config.size \
               + '!= null">\n            ' \
                 'limit #{' + Config.offset + '},#{' + Config.size + '}\n        </if>'
        need = "${orderByClause}"
        pre = 0
        while True:
            index = content.find(need, pre + len(need))
            if index == -1 or index == pre:
                break
            pre = index
            if content.find('limit #{' + Config.offset + '},#{' + Config.size + '}', index) != -1:
                continue
            index = content.find(">", index) + 1
            content = content[:index] + data + content[index:]
        self._write_str_to_file(path, content)

    @staticmethod
    def _read_file_to_str(path):
        s = ""
        with open(path, encoding="utf-8") as f:
            for i in f.readlines():
                s += i
        return s

    @staticmethod
    def _write_str_to_file(path, content):
        with open(path, 'w') as f:
            f.write(content)

    @staticmethod
    def _set_variable(content, variable, key):
        index = content.find(key)
        suffix = content[index + len(key) + len(' targetPackage="'):]
        index_suffix_tail = suffix.find("\"")
        suffix_t = suffix[:index_suffix_tail]
        prefix = suffix[index_suffix_tail + len(' targetPackage="') + 1:]
        index_prefix_tail = prefix.find("\"")
        prefix_t = prefix[:index_prefix_tail] + "/"
        setattr(Config, variable, prefix_t + "/".join(suffix_t.split(".")))


if __name__ == '__main__':
    MybatisGen().gen()
