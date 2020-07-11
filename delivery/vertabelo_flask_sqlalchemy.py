#! /usr/bin/python

import re
import sys
import getopt
import os
from xml.dom import minidom
from xml.dom import Node

debugEnabled = os.getenv("DEBUG", "0")

#################################################################


class CodeEmiter:

    indentLevel = 0
    indentContent = "    "
    endLineContent = "\n"

    output = u""

    def indent(self):
        self.indentLevel += 1

    def deindent(self):
        self.indentLevel -= 1

    def emit(self, content):
        self.output += (
            (self.indentContent * self.indentLevel)
            + content
            + self.endLineContent
        )

    def comment(self, content):

        if content == None or content == "":
            return

        lines = content.split(self.endLineContent)
        for line in lines:
            self.emit("# " + line)

    def nl(self):
        self.output += self.endLineContent

    def vspace(self):
        self.nl()
        self.nl()
        self.nl()

    def code(self):
        return self.output.encode("utf-8")


# Vertabelo model as object model


class Column:

    name = None
    sql_type = None
    is_pk = False
    description = None
    is_fk = False
    table = None

    def column_with_table_name(self):
        return self.table.name + "." + self.name

    def __repr__(self):
        return "<Column(name='%s' type='%s' pk='%s')>" % (
            self.name,
            self.sql_type,
            self.is_pk,
        )

    def dump(self):
        print(str(self))


class Table:

    dbModel = None

    id = None
    name = None
    columns = None
    references = None

    def __init__(self):
        self.columns = []
        self.fk_references = []
        self.pk_references = []

    def findColumn(self, id):

        for i in self.columns:
            if i.id == id:
                return i

        raise Exception(
            "Database model is corrupted. Couldn't find column with id: " + id
        )

    def __repr__(self):
        return "<Table(name='%s') columns=%d>" % (self.name, len(self.columns))

    def dump(self):
        print(str(self))
        for i in self.columns:
            i.dump()


class View:
    name = None


class Reference:

    dbModel = None
    name = None

    pk_table = None
    fk_table = None

    pk_role = None
    fk_role = None

    fk_columns = None
    pk_columns = None

    def __init__(self):
        self.fk_columns = []
        self.pk_columns = []
        self.name = ""

    def __repr__(self):
        return "<Reference(name='%s')>" % (self.name)

    def dump(self):
        print(str(self))


class DbModel:

    tables = None
    references = None
    views = None

    def __init__(self):
        self.tables = []
        self.references = []
        self.views = []

    def findTable(self, id):
        for i in self.tables:
            if i.id == id:
                return i

        raise Exception(
            "Database model is corrupted. Couldn't find table with id: " + id
        )

    def dump(self):
        print("Model")
        for i in self.tables:
            i.dump()


# Vertabelo 2.2 builder,
# builds a Vertabelo object model by parsing XML (version 2.2)


def find_subnode_by_name(node, sub_name):
    for i in node.childNodes:
        if i.nodeName == sub_name:
            return i
    raise Exception("couldn't find tag '%s' in '%s'" % (sub_name, node))


def subnode_value(node, sub_name):
    node = find_subnode_by_name(node, sub_name)

    if node.firstChild == None:
        return ""

    return node.firstChild.nodeValue


class DbModelBuilder_v2_2:
    def buildReference(self, reference, xmlNode):

        reference.id = xmlNode.attributes["Id"].value

        reference.name = subnode_value(xmlNode, "Name")
        reference.description = subnode_value(xmlNode, "Description")

        pkTableId = subnode_value(xmlNode, "PKTable")
        fkTableId = subnode_value(xmlNode, "FKTable")

        reference.pk_role = subnode_value(xmlNode, "PKRole")
        reference.fk_role = subnode_value(xmlNode, "FKRole")

        reference.pk_table = reference.dbModel.findTable(pkTableId)
        reference.fk_table = reference.dbModel.findTable(fkTableId)

        reference.pk_table.pk_references.append(reference)
        reference.fk_table.fk_references.append(reference)

        references = xmlNode.getElementsByTagName("ReferenceColumns")[0]

        for i in references.childNodes:
            if i.nodeType == Node.ELEMENT_NODE:

                pkColumnId = subnode_value(i, "PKColumn")
                fkColumnId = subnode_value(i, "FKColumn")

                pk_column = reference.pk_table.findColumn(pkColumnId)
                fk_column = reference.fk_table.findColumn(fkColumnId)

                reference.pk_columns.append(pk_column)
                reference.fk_columns.append(fk_column)

                fk_column.is_fk = True
                fk_column.pk_column = pk_column

    def buildTable(self, table, xmlNode):
        table.id = xmlNode.attributes["Id"].value

        table.name = subnode_value(xmlNode, "Name")
        table.description = subnode_value(xmlNode, "Description")

        columns = find_subnode_by_name(xmlNode, "Columns").childNodes

        for i in columns:
            if i.nodeType == Node.ELEMENT_NODE:
                c = Column()
                self.buildColumn(c, i)
                c.table = table
                table.columns.append(c)

    def buildColumn(self, column, xmlNode):
        column.id = xmlNode.attributes["Id"].value

        column.name = subnode_value(xmlNode, "Name")
        column.sql_type = subnode_value(xmlNode, "Type")
        pk = subnode_value(xmlNode, "PK")

        if pk == "true":
            column.is_pk = True
        else:
            column.is_pk = False

        column.description = subnode_value(xmlNode, "Description")
        return column

    def build(self, xmlRoot):

        dbModel = DbModel()

        tables = xmlRoot.getElementsByTagName("Tables")[0]

        for i in tables.childNodes:
            if i.nodeType == Node.ELEMENT_NODE:
                t = Table()
                t.dbModel = dbModel
                self.buildTable(t, i)
                dbModel.tables.append(t)

        references = xmlRoot.getElementsByTagName("References")[0]

        for i in references.childNodes:
            if i.nodeType == Node.ELEMENT_NODE:
                r = Reference()
                r.dbModel = dbModel
                self.buildReference(r, i)
                dbModel.references.append(r)

        return dbModel


#
# Instead of inherintance we using just copy and paste.
#


class DbModelBuilder_v2_3:
    def buildReference(self, reference, xmlNode):

        reference.id = xmlNode.attributes["Id"].value

        reference.name = subnode_value(xmlNode, "Name")
        reference.description = subnode_value(xmlNode, "Description")

        pkTableId = subnode_value(xmlNode, "PKTable")
        fkTableId = subnode_value(xmlNode, "FKTable")

        reference.pk_role = subnode_value(xmlNode, "PKRole")
        reference.fk_role = subnode_value(xmlNode, "FKRole")

        reference.pk_table = reference.dbModel.findTable(pkTableId)
        reference.fk_table = reference.dbModel.findTable(fkTableId)

        reference.pk_table.pk_references.append(reference)
        reference.fk_table.fk_references.append(reference)

        references = xmlNode.getElementsByTagName("ReferenceColumns")[0]

        for i in references.childNodes:
            if i.nodeType == Node.ELEMENT_NODE:

                pkColumnId = subnode_value(i, "PKColumn")
                fkColumnId = subnode_value(i, "FKColumn")

                pk_column = reference.pk_table.findColumn(pkColumnId)
                fk_column = reference.fk_table.findColumn(fkColumnId)

                reference.pk_columns.append(pk_column)
                reference.fk_columns.append(fk_column)

                fk_column.is_fk = True
                fk_column.pk_column = pk_column

    def buildTable(self, table, xmlNode):
        table.id = xmlNode.attributes["Id"].value

        table.name = subnode_value(xmlNode, "Name")
        table.description = subnode_value(xmlNode, "Description")

        columns = find_subnode_by_name(xmlNode, "Columns").childNodes

        pkColumnIds = self.pkColumnIds(xmlNode)

        for i in columns:
            if i.nodeType == Node.ELEMENT_NODE:
                c = Column()
                self.buildColumn(c, pkColumnIds, i)
                c.table = table
                table.columns.append(c)

    def pkColumnIds(self, xmlNode):

        res = set()

        primaryKey = find_subnode_by_name(xmlNode, "PrimaryKey")

        primaryKeyColumns = find_subnode_by_name(
            primaryKey, "Columns"
        ).childNodes

        for i in primaryKeyColumns:
            if i.nodeType == Node.ELEMENT_NODE:
                columnId = i.firstChild.nodeValue
                res.add(columnId)

        return res

    def buildColumn(self, column, pkColumnIds, xmlNode):
        column.id = xmlNode.attributes["Id"].value

        column.name = subnode_value(xmlNode, "Name")
        column.sql_type = subnode_value(xmlNode, "Type")

        column.description = subnode_value(xmlNode, "Description")

        if column.id in pkColumnIds:
            column.is_pk = True
        else:
            column.is_pk = False

        return column

    def build(self, xmlRoot):

        dbModel = DbModel()

        tables = xmlRoot.getElementsByTagName("Tables")[0]

        for i in tables.childNodes:
            if i.nodeType == Node.ELEMENT_NODE:
                t = Table()
                t.dbModel = dbModel
                self.buildTable(t, i)
                dbModel.tables.append(t)

        references = xmlRoot.getElementsByTagName("References")[0]

        for i in references.childNodes:
            if i.nodeType == Node.ELEMENT_NODE:
                r = Reference()
                r.dbModel = dbModel
                self.buildReference(r, i)
                dbModel.references.append(r)

        return dbModel


#################################################################

# SQLAlchemy model.


def to_camelcase(s):
    return re.sub(r"(?!^)_([a-zA-Z])", lambda m: m.group(1).upper(), s)


def sa_class_name(sql_name):
    return "".join([x.capitalize() for x in sql_name.split("_")])


def sa_property_name(sql_name):
    return sql_name.lower()


class SaColumn:
    name = None
    column_name = None
    python_type = None
    is_pk = False
    description = None
    fk_table_column = None
    is_deferred = False

    def emit(self, emiter):

        extraParams = ""

        if self.fk_table_column is not None:
            extraParams += ", db.ForeignKey('%s')" % (self.fk_table_column)

        if self.is_pk:
            extraParams += ", primary_key=True"

        emiter.comment(self.description)

        if self.is_deferred:
            template = "%s = deferred(Column('%s', %s%s))"
        else:
            template = "%s = db.Column('%s', %s%s)"

        emiter.emit(
            template
            % (
                self.name,
                self.column_name,
                "db." + self.python_type,
                extraParams,
            )
        )


class SaRelationship:
    role = ""
    class_name = ""
    backref = ""
    foreign_keys = ""

    def emit(self, emiter):
        if self.backref is None:
            emiter.emit(
                "%s = db.relationship('%s', foreign_keys=%s)"
                % (self.role, self.class_name, self.foreign_keys)
            )
        else:
            emiter.emit(
                "%s = db.relationship('%s', backref='%s',foreign_keys=%s)"
                % (self.role, self.class_name, self.backref, self.foreign_keys)
            )


class SaTable:
    description = ""
    name = None
    columns = None
    relationships = None

    def __init__(self):
        self.columns = []
        self.relationships = []

    def emit(self, emiter):
        emiter.comment("name " + self.name)


class SaClass:

    name = None
    table_name = None
    description = None
    columns = None
    relationships = None

    def __init__(self):
        self.columns = []
        self.relationships = []

    def emit(self, emiter):
        emiter.comment(self.description)
        emiter.emit("class %s(db.Model):" % (self.name))
        emiter.indent()
        emiter.emit('__tablename__ = "%s"' % (self.table_name))

        for c in self.columns:
            c.emit(emiter)

        if len(self.relationships) > 0:
            emiter.nl()
            for r in self.relationships:
                r.emit(emiter)

        emiter.deindent()


class SaModel:

    elements = None

    def __init__(self):
        self.elements = []

    def emit(self, emiter):
        emiter.comment("-*- encoding: utf-8 -*-")
        # emiter.comment("begin")
        emiter.nl()
        emiter.emit("from flask import Flask")
        emiter.emit("from flask_sqlalchemy import SQLAlchemy")
        emiter.nl()
        emiter.emit("app = Flask(__name__)")
        emiter.emit("db = SQLAlchemy(app)")
        # emiter.vspace()
        emiter.nl()

        for t in self.elements:
            t.emit(emiter)
            emiter.nl()

        # emiter.comment("end")


# FIXME add type mapping for every supported database engine
# this is a temporary solution

string_sql_types = set(["varchar", "char", "nchar", "nvarchar"])
integer_sql_types = set(["int", "int4", "integer", "serial"])
float_sql_type = set(["real", "float"])
big_integer_sql_types = set(["numeric", "decimal"])
blob_sql_types = set(["oid", "blob"])
clob_sql_types = set(["text", "clob"])
datetime_sql_types = set(["datetime"])
timestamp_sql_types = set(["timestamp"])
date_sql_types = set(["date"])
bool_sql_types = set(["bool", "boolean"])


class Generator:

    root = None
    dbModel = None
    saModel = None

    def parse(self, xmlString):
        self.root = minidom.parseString(xmlString)

    def guessType(self, type):

        type = type.lower()

        # strip type parameters 'varchar(100)' -> 'varchar'
        type = type.split("(")[0]

        if type in string_sql_types:
            return "Unicode"

        if type in integer_sql_types:
            return "Integer"

        if type in float_sql_type:
            return "Float"

        if type in big_integer_sql_types:
            return "Numeric"

        if type in blob_sql_types:
            return "LargeBinary"

        if type in clob_sql_types:
            return "Text"

        if type in datetime_sql_types:
            return "DateTime"

        if type in date_sql_types:
            return "Date"

        if type in timestamp_sql_types:
            return "Time"

        if type in bool_sql_types:
            return "Boolean"

        return None

    def is_deferred(self, python_type):

        if python_type == "Text" or python_type == "LargeBinary":
            return True

        return False

    def processColumn(self, column):
        res = SaColumn()
        res.name = sa_property_name(column.name)
        res.column_name = column.name
        res.python_type = self.guessType(column.sql_type)
        res.description = column.description
        res.is_pk = column.is_pk

        if column.is_fk:
            res.fk_table_column = column.pk_column.column_with_table_name()

        if res.python_type == None:
            warn = "Unknown SQL type: '%s' " % (column.sql_type)
            # print column.table.name, column.name, warn
            res.description += warn
            res.python_type = "String"

        res.is_deferred = self.is_deferred(res.python_type)

        return res

    def processReference(self, reference):

        # FIXME add support for multiple columns reference
        if len(reference.fk_columns) > 1:
            return None

        res = SaRelationship()
        role = reference.fk_role
        backref = reference.pk_role
        sa_property = reference.fk_columns[0].name

        if role == "":
            role = reference.pk_table.name

        if backref == "":
            backref = None
        else:
            backref = reference.fk_table.name + "_" + backref

        res.role = sa_property_name(role)
        res.class_name = sa_class_name(reference.pk_table.name)

        if backref == None:
            res.backref = None
        else:
            res.backref = sa_property_name(backref)

        res.foreign_keys = sa_property_name(sa_property)

        return res

    def processTable(self, table):

        res = SaClass()

        res.name = sa_class_name(table.name)
        res.table_name = table.name
        res.description = table.description

        for i in table.columns:
            res.columns.append(self.processColumn(i))

        for i in table.fk_references:
            r = self.processReference(i)
            if r != None:
                res.relationships.append(r)

        return res

    def process(self):

        databaseModel = self.root.getElementsByTagName("DatabaseModel")

        if len(databaseModel) == 0:
            raise Exception("This is not a Vertabelo XML file.")

        version = databaseModel[0].attributes["VersionId"].value

        if version == "2.2":
            builder = DbModelBuilder_v2_2()
        elif version == "2.3":
            builder = DbModelBuilder_v2_3()
        else:
            raise Exception(
                "Not supported Vertabelo XML format version %s" % (version)
            )

        self.dbModel = builder.build(self.root)

        self.saModel = SaModel()

        for i in self.dbModel.tables:
            self.saModel.elements.append(self.processTable(i))

    def code(self):
        emiter = CodeEmiter()
        self.saModel.emit(emiter)
        return emiter.code()


def generate(xmlFile, pyFile):
    inf = open(xmlFile, "r")
    xml = inf.read()

    g = Generator()
    g.parse(xml)
    g.process()

    if debugEnabled == "1":
        g.dbModel.dump()

    outf = open(pyFile, "wb")
    outf.write(g.code())
    outf.close()


def main(argv):
    inputfile = "model.xml"
    outputfile = "model.py"

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("vertabelo_flask_sqlalchemy.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(
                "vertabelo_flask_sqlalchemy.py -i <inputfile> -o <outputfile>"
            )
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    generate(inputfile, outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
