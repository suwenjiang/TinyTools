#-*- coding:gbk -*-
from xlwt import Workbook, Style, Formula
import re
import os
import argparse
import sys

def get_formatted_in_a_file(path):
    try:
        with open(path) as file:
            allmsg = file.read()

            if "</" not in allmsg and '>' not in allmsg:
                print ("unable to retrieve the log file")
                return []
            text0 = allmsg.split('</')[0].split('>')
            all_formatted_msg = []
            # text0 format [<Msg time="" type="" code="" source="" process="" thread="" methodName="" machine="" user="" elapsed=""', "msg..."]
            msg1 = re.findall('"([^"]*)"', text0[0])
            msg1.append(text0[1])

            all_formatted_msg.append(msg1)
            # the other lines
            for i in allmsg.split('</')[1:-1]:
                msg2 = i.split('>')[1:]
                formatted_msg2 = re.findall('"([^"]*)"', msg2[0])
                formatted_msg2.append(msg2[1])
                all_formatted_msg.append(formatted_msg2)
        return sorted(all_formatted_msg, key=lambda item: item[1])
    except Exception as msg:
        print (msg)
        return []


def Write_To_excel(book, sheetName, sorted_list):
    try:
        sheet1 = book.add_sheet(sheetName, cell_overwrite_ok=True)
        # create column
        row0 = sheet1.row(0)
        row0.write(0, 'ID')
        row0.write(1, 'TIME')
        row0.write(2, 'TYPE')
        row0.write(3, 'CODE')
        row0.write(4, 'SOURCE')
        row0.write(5, 'PROCESS')
        row0.write(6, 'THREAD')
        row0.write(7, 'METHODNAME')
        row0.write(8, 'MACHINE')
        row0.write(9, 'USER')
        row0.write(10, 'ELAPSED')
        row0.write(11, 'MESSAGE')
        row_count = 1
        for item in sorted_list:
            column_count = 0
            new_row = sheet1.row(row_count)
            new_row.write(0, row_count)  # every 0 column was the row_count
            for val in item:
                column_count = column_count + 1
                new_row.write(column_count, val)

            row_count = row_count + 1
    except Exception as msg:
        print ("write to excel" + msg)


def get_logfile_in_dir(log_path):
    try:
        fileslList = []
        for root, dirname, files in os.walk(log_path):
            # print root,dir,files
            for file in files:
                # print file
                if os.path.splitext(file)[1] == '.log':
                    filePath = os.path.join(root, file)
                    if os.path.getsize(filePath) != 0:
                        fileslList.append(filePath)
        return fileslList
    except IOError as msg:
        print (msg)


def main(logfiles,dir_path):

    if len(logfiles) != 0:
        book = Workbook('utf-8')
        # crate the cover sheet
        sheet0 = book.add_sheet('Cover', cell_overwrite_ok=True)
        row0 = sheet0.row(0)
        row0.write(0, "ID")
        row0.write(1, "FILE")
        row0.write(2, "SHEET")
        tall_style = Style.easyxf('font:height 72;')
        row0.set_style(tall_style)
        sheet0.col(1).width = 256 * 50
        for item in logfiles:
            print ("processed file:" + os.path.split(item)[1])
            new_row = sheet0.row(logfiles.index(item) + 1)
            new_row.write(0, logfiles.index(item) + 1)

            click = '#sheet%s!A1' % str(logfiles.index(item))
            text = os.path.split(item)[1]
            style = Style.easyxf('font: underline single,color blue;')
            new_row.write(1, Formula('HYPERLINK("%s";"%s")' % (click, text)), style)
            new_row.write(2, 'sheet' + str(logfiles.index(item)))
            # creat other sheet
            out_putlist = get_formatted_in_a_file(item)
            Write_To_excel(book, 'sheet' + str(logfiles.index(item)), out_putlist)

        save_path = os.path.join(dir_path, 'Aresult.xls')
        book.save(save_path)
    else:
        print ("the dirtory doesn't contains any log file")


if __name__ == '__main__':
    logfiles = []
    parser = argparse.ArgumentParser(description='Format the arcgis server or portal logs.')
    parser.add_argument('f',
                    help='Directory of log file or single log file')

    args = parser.parse_args()
    if os.path.isdir(args.f):
        logfiles = get_logfile_in_dir(args.f)
        main(logfiles,args.f)
        print ("formatted result created")
    elif '.log' in args.f:
        logfiles.append(args.f)
        main(logfiles,os.path.split(args.f)[0])
        print ("formatted result created")
    else:
        print ("please input a valid log directory or file")
        sys.exit()


