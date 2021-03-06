from statistics import mode
from class_module import *
from class_line import *
from func import *


def read_section_name(line):  # ? delete??
    temp = line.content
    if temp.find('(') != -1:  # '(' exist
        name = temp[temp.find('module') + len('module') + 1:temp.find('(')]
    else:  # '(' don't exist
        name = temp[temp.find('module') + len('module') + 1:]

    return name


# * fatals: 
# duplicate name
# negative values in define size
# float values in define size
# too large define size
def append_defines(lines, module):

    for line_num, curr_line in enumerate(lines):
        line = Line(curr_line)
        line.erase_comment()
        if line.is_define_section():
            param = Param()
            temp = line.content.replace('\t', ' ')

            temp = temp.replace('`define', '')
            temp = re.sub("[;|\t|,]", "", temp).strip()
            temp_name, temp_size = temp.split(' ')

            if str(temp_size).isdigit() and int(temp_size) > 0 and int(temp_size) < 100000:
                param.name = '`' + temp_name
                param.value = int(temp_size)
            else:
                print("fatal: parameter '%s' must be positive integer and less than 100000, line %i\n" % (temp_name, line_num + 1))
                exit()

            for par in module.params:
                if par.name == param.name:
                    print("fatal: duplicate parameter '%s', line %i\n" % (temp_name, line_num + 1))
                    exit()

            module.append_params(param)
            continue

        elif line.is_module_section():
            break


# * fatals: 
# duplicate name
# unknown mathematical operation in parameter size
# unknown subparameter in parameter size
# negative values in parameter size
# float values in parameter size
# difficult expression in parameter size
# too large parameter size
# too large argument in '<<' operation
def read_section_params(line, param_list, line_num):
    param = Param()

    temp = line.content.replace('\t', ' ')
    temp = temp.replace('parameter', '')
    temp = re.sub("[;| |\t|,]", "", temp)
    
    temp_name, temp_expr = temp.split('=')

    for par in param_list:
        if par.name == temp_name:
            print("fatal: duplicate parameter '%s', line %i\n" % (temp_name, line_num + 1))
            exit()

    # * parametric size of parameter
    if not is_number(temp_expr):

        if '<<' in temp_expr:
            val_left, val_right = temp_expr.split('<<')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check += 1
                        break
            else:
                check += 1

            # check if every parameter is a number now
            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                if int(val_right) > 20:
                    print("fatal: the argument is too large. Parameter '%s', line %i\n" % (temp_name, line_num + 1))
                    exit()
                else:
                    temp_size = int(val_left) << int(val_right)
            else:
                print("fatal: arguments in '<<' operation must be positive integer. Parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

        elif '>>' in temp_expr:
            val_left, val_right = temp_expr.split('>>')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) >> int(val_right)
            else:
                print("fatal: arguments in '>>' operation must be positive integer. Parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()
            
        elif '+' in temp_expr:
            val_left, val_right = temp_expr.split('+')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) + int(val_right)
            else:
                print("fatal: arguments in '+' must be positive integer. Parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()    

        elif '-' in temp_expr:
            val_left, val_right = temp_expr.split('-')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) - int(val_right)
            else:
                print("fatal: arguments in '-' must be positive integer. Parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

        elif '*' in temp_expr:
            val_left, val_right = temp_expr.split('*')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                temp_size = int(val_left) * int(val_right)
            else:
                print("fatal: arguments in '*' must be positive integer. Parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

        elif '/' in temp_expr:
            val_left, val_right = temp_expr.split('/')
            check = 0

            if not is_number(val_left):
                for par in param_list:
                    if val_left == par.name:
                        val_left = par.value
                        check += 1
                        break
            else:
                check += 1
                
            if not is_number(val_right):
                for par in param_list:
                    if val_right == par.name:
                        val_right = par.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in size of parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

            if str(val_left).isdigit() and str(val_right).isdigit():
                if int(val_left) % int(val_right) == 0:
                    temp_size = int(int(val_left) / int(val_right))
                else:
                    print("fatal: parameter '%s' must be positive integer, line %i\n" % (temp_name, line_num + 1))
                    exit()
            else:
                print("fatal: unknown expression in size of parameter '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

        else:
            print("fatal: unknown expression in parameter value %s, line %i\n" % (temp_name, line_num + 1))
            exit()
    
    # * simple parameter size
    else:
        temp_size = temp_expr

    if str(temp_size).isdigit() and int(temp_size) > 0 and int(temp_size) < 100000:
        param.name =  temp_name
        param.value = int(temp_size)
    else:
        print("fatal: parameter '%s' must be positive integer and less than 100000, line %i\n" % (temp_name, line_num + 1))
        exit()
    
    return param


# * fatals:
# duplicate name
# unknown parameter in pin size
# negative pin size
# negitive pin size values
# unknown expression in pin size values (not +/-) => unknown parameter
# float pin size
# * warnings:
# equal limits in pin size
def read_section_pins(line, param_list, pin_list, line_num):
    pin_arr = []
    pin_direction = 'NaN'
    k = 1

    temp = line.content.strip().replace('\t', ' ')

    temp_direction_name = re.sub(r'\[[^()]*\]', '', temp) # substracting size

    pin_direction = temp_direction_name[:temp_direction_name.find(' ')] # input | output | inout

    pin_size = temp[temp.find('['):temp.find(']') + 1] # [...]
    
    temp_name = temp_direction_name.replace(pin_direction, '')
    temp_name = temp_name.replace('reg', '').replace('wire', '') #? also delete SystemVerilog's 'logic'?
    temp_name = re.sub("[;| |\t]", "", temp_name) # name1,name2,..
    temp_name_arr = temp_name.split(',')
    temp_name_arr = list(filter(None, temp_name_arr))  # deleting '' names
    # print('temp_name_arr:', temp_name_arr) # names array

    for pin in pin_list:
        for name in temp_name_arr:
            if pin.name == name:
                print("fatal: duplicate pin name '%s', line %i\n" % (name, line_num + 1))
                exit()    

    # * parametric size
    if pin_size:

        pin_size = re.sub("[\[|\]| |\t]", "", pin_size)  # deleting [] and whitespaces
        temp_size_arr = pin_size.split(':')
        start_val, end_val = temp_size_arr
        # print('temp_size_arr:', temp_size_arr) # sizes array

        if not is_number(start_val):  # if parameter in LEFT part

            if '-' in start_val:
                start_val = start_val.split('-')
                start_val_left, start_val_right = start_val
                k = -1
            elif '+' in start_val:
                start_val = start_val.split('+')
                start_val_left, start_val_right = start_val
                k = 1
            else:
                start_val_left = start_val
                start_val_right = 0
                k = 1

            check = 0

            if not is_number(start_val_left):  # parameter in left subpart
                for param in param_list:
                    if param.name == start_val_left:
                        start_val_left = param.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(start_val_right):  # parameter in right subpart
                for param in param_list:
                    if param.name == start_val_right:
                        start_val_right = param.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in pin size, line %i\n" % (line_num + 1))
                exit()
            
            if str(start_val_left).isdigit() and str(start_val_right).isdigit():
                start_val = int(start_val_left) + k * int(start_val_right) 
                if start_val < 0:
                    print("fatal: arguments in size must be !positive integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
                    exit()
            else:
                print("fatal: arguments in size must be positive !integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

        if not is_number(end_val):  # if parameter in RIGHT part

            if '-' in end_val:
                end_val = end_val.split('-')
                end_val_left, end_val_right = end_val
                k = -1
            elif '+' in end_val:
                end_val = end_val.split('+')
                end_val_left, end_val_right = end_val
                k = 1
            else:
                end_val_left = end_val
                end_val_right = 0
                k = 1

            check = 0

            if not is_number(end_val_left):  # parameter in left subpart
                for param in param_list:
                    if param.name == end_val_left:
                        end_val_left = param.value
                        check += 1
                        break
            else:
                check += 1

            if not is_number(end_val_right):  # parameter in right subpart
                for param in param_list:
                    if param.name == end_val_right:
                        end_val_right = param.value
                        check += 1
                        break
            else:
                check += 1

            if check < 2:
                print("fatal: unknown parameter in pin size, line %i\n" % (line_num + 1))
                exit()

            if str(start_val_left).isdigit() and str(start_val_right).isdigit():
                end_val = int(end_val_left) + k * int(end_val_right)
                if end_val < 0:
                    print("fatal: arguments in size must be !positive integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
                    exit()
            else:
                print("fatal: arguments in size must be positive !integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
                exit()

        if int(start_val) < 0 or int(end_val) < 0:
            print("fatal: limits must be positive integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
            exit()

        if start_val == end_val:
            print("warning: equal limits in the pin size. Pin '%s', line %i\n" % (temp_name, line_num + 1))

        pin_true_size = int(start_val) - int(end_val) + 1

        if pin_true_size < 1:
            print("fatal: pin size must be positive integer. Pin '%s', line %i\n" % (temp_name, line_num + 1))
            exit()

    # * simple size (=1)
    else:
        pin_true_size = 1

    for pin_name in temp_name_arr:
        pin = Pin(pin_name, pin_direction, pin_true_size)
        pin_arr.append(pin)

    return pin_arr


#* fatals:
# no modules in file
# duplicate module name
# two or more modules modules have the maximum number of attachments
#* warning:
# two or more non-callable modules. Top module will be chosen as module with the most attachments
def get_top_module(lines):
    top_module_name = 'NaN'
    module_list = []

    # collecting module names and it's content
    module_fs = Module_for_search() #TODO ?????????? ?????? ???????????????? ???????????????
    temp_name = ''

    for line_num, line in enumerate(lines):
        line = line.replace('\t', ' ')
        if '//' in line:
            line = line[:line.find('//')]

        if ('module' in line or 'macromodule' in line) and not 'endmodule' in line:
            module_fs = Module_for_search()
            temp_name = ''
            start_line = line_num

        temp_line = line.strip()
        module_fs.text += temp_line + ' '
        module_fs.text_arr.append(temp_line)

        if not module_fs.name:
            temp_name += temp_line + ' '
            if ';' in temp_line:
                temp_name = re.sub(r'\([^()]*\)', '', temp_name)
                temp_name = temp_name.replace('module', '')
                temp_name = re.sub('[;| ]', '', temp_name)
                module_fs.name = temp_name
                temp_name = ''

        if 'endmodule' in temp_line:
            for mod in module_list:
                if mod.name == module_fs.name:
                    print("fatal: duplicate module name '%s', line %i\n" % (module_fs.name, start_line + 1))
                    exit() 

            module_list.append(module_fs)
            module_fs = Module_for_search()
    
    if not module_list:
        print('fatal: no modules in file\n')
        exit()


    # searching attachmnets in each module
    for mod in module_list:
        for submod in module_list:
            if submod.name in mod.text and submod.name != mod.name and submod.name not in mod.attachments:
                mod.attachments.append(submod.name)
                mod.count_att += 1
                submod.called = True
    
    max_att = -1
    count_non_callable = 0
    for mod in module_list:
        if not mod.called:
            count_non_callable += 1
            # print(mod.name)
            if mod.count_att > max_att:
                max_att = mod.count_att

    if count_non_callable > 1:
        print('warning: there are two or more non-callable modules. Top module will be chosen as module with the most attachments\n')


    # choosing top module as non-callable module
    count_top = 0
    for mod in module_list:
        if not mod.called and mod.count_att == max_att:
            top_module_name = mod
            count_top += 1

    if count_top > 1:
        print('fatal: there are two or more non-callable modules modules have the maximum number of attachments\n')
        exit()

    return top_module_name
