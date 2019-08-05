import DataGenerator as dg
import DataValidator as dv
import PaymentCalculator as pc
import datetime as dt
import pandas as pd
import numpy as np
import utilities as ut
import pickle
import matplotlib.pyplot as pyplot

def stage1(seed):
    data_generator = dg.DataGenerator(seed)
    data_stage1 = data_generator.get_records()
    valuation_date_stage1 = dt.datetime.now()
    file_name = '_'.join(['InputData', ut.get_seeded_file_name(seed, valuation_date_stage1)])
    ut.write_csv_file(file_name, data_stage1)
    return file_name


def stage2(file_name_stage1):
    readed_data_stage1 = pd.read_csv(file_name_stage1)
    data_validator = dv.DataValidator(readed_data_stage1)
    data_stage2 = data_validator.get_mapped_data()
    file_name_stage2 = 'Mapped' + file_name_stage1
    np.save(file_name_stage2, data_stage2)
    return file_name_stage2 + '.npy'


def stage3(seed, file_name_stage2):
    readed_data_stage2 = np.load(file_name_stage2, allow_pickle=True)
    payment_calculator = pc.PaymentCalculator(readed_data_stage2)
    data_stage3 = payment_calculator.get_projections()
    valuation_date_stage3 = dt.datetime.now()
    file_name_stage3 = '_'.join(['LoanData', ut.get_seeded_file_name(seed, valuation_date_stage3)])
    
    with open(file_name_stage3, 'wb') as file:
        pickle.dump(data_stage3, file)

    return file_name_stage3


def vizualise_loan_per_program(id_person, id_program, data):
    projections = data[id_person][id_program]
    x_data = range(len(projections))
    y_data = projections
    pyplot.scatter(x_data,y_data)
    pyplot.title('Growth of loan for person #{} in program #{}'.format(id_person, id_program))
    pyplot.show() 
    

def get_data_stage3(file_name):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
        
    return data

  
def main():
    #1 part
    seed = 13
    file_name_stage1 = stage1(seed)
    #2 part
    file_name_stage2 = stage2(file_name_stage1)   
    #3 part
    file_name_stage3 = stage3(seed, file_name_stage2)
    data_stage3 = get_data_stage3(file_name_stage3)
    
    id_person = list(data_stage3.keys())[0]
    id_program = list(data_stage3[id_person].keys())[0]
    vizualise_loan_per_program(id_person, id_program, data_stage3)
    
    
if __name__ == '__main__':
    main()