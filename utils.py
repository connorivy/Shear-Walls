def ft_inches_to_decimal(ft, inches):
        return ft + inches / 12

def write_to_revit():
    tran = DB.Transaction(doc)
    if tran.Start('edit model shearwalls') == DB.TransactionStatus.Started:

        bic = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_DetailComponents).OfClass(DB.FamilyInstance).ToElements()
        swp = []
        for x in bic:
            try:
                if x.Name == 'Shear Wall Plan':
                    swp.append(x)
            except:
                continue

        blank_count = 0
        
        with open('P:\\\\Structural\\2021\\2115 - Dallas\\2115.147 Toll Brothers Addison Road\\5 - Project Documents\B - Calculations\CI\Wood Calcs\Shear Walls\\toll_brothers_shear_wall_input1.txt') as f:
            lines = f.readlines() 

        for line in lines:
            line = line.split()
            print(line, len(swp))

            if len(line) == 0:
                blank_count += 1
                if blank_count > 3:
                    break
                continue
            if len(line) != 16:
                continue
            else:
                blank_count = 0

            match_found = False

            # only assign shear wall if we have a valid design for it
            if line['15'].isdigit():
                for index in range(len(swp)):
                    # please don't mess with level 2, that one is done
                    if assert_almost_equal(swp[index].Location.Curve.GetEndPoint(0).Z, 14.739583333):
                        continue
                    if not assert_almost_equal(swp[index].Location.Curve.GetEndPoint(0).X, float(line[7])):
                        continue
                    if not assert_almost_equal(swp[index].Location.Curve.GetEndPoint(0).Y,float(line[8])):
                        continue
                    if not assert_almost_equal(swp[index].Location.Curve.GetEndPoint(0).Z,float(line[9])):
                        continue
                    
                    match_found = True
                    swp[index].GetParameters('SW #')[0].Set(line[15])
                    swp.pop(index)
                    break
        
            if not match_found:
                print(f'Shear wall was not updated for {line[0]} at lvl {line[1]}')
        
        try:
            if DB.TransactionStatus.Committed == tran.Commit():
                print('changes were successfully made')
            else:
                print('changes could not be made')
                tran.RollBack()
        except:
            print('changes could not be made')
            tran.RollBack()

def assert_almost_equal(x1, x2):
    if abs(x1-x2) < .00000001:
        return True
    else:
        return False
