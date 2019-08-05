import numpy as np
import pandas as pd

from mimesis import Person
from mimesis.providers.payment import Payment
from mimesis.enums import Gender, CardType
from mimesis.schema import Schema

class DataGenerator:
    
    def __init__(self, seed=13, similar_people_count=5, max_repeat_count=12):
        self._initialize_counts_seed(seed, similar_people_count, max_repeat_count)
        
        self.df_people = self._generate_people() 
        self.df_cards = self._generate_cards()
        self.df_records = pd.merge(self.df_people, self.df_cards, left_on='id_person', right_on='id_person')
        
    
    def _initialize_counts_seed(self, seed, similar_people_count, max_repeat_count):
        self.seed = seed
        self.similar_people_count = similar_people_count
        self.max_repeat_count = max_repeat_count
        self.records_count = self._compute_records_count()
        np.random.seed(self.seed)
        self.person = Person('en', seed = self.seed)
        self.payment = Payment(seed = self.seed)
        
        
    def _compute_records_count(self):
        num_records = 0
        for i in range(1, self.max_repeat_count+1):
            num_records += i*self.similar_people_count
            
        return num_records  
    
    def get_records(self):
        return self.df_records
       
        
    def _generate_cards(self):
        person_ids = iter(self._generate_ids())
        int_loans = np.random.randint(1, 101, self.records_count)
        float_loans = np.array(int_loans*1000, np.float64)
        loans = iter(float_loans)
        
        description_c = (
            lambda: {
            'id_person': next(person_ids),
            'credit_card_num': self.payment.credit_card_number(card_type=CardType.VISA),
            'credit_card_exp_date': self.payment.credit_card_expiration_date(maximum=21, minimum=19),
            'loan': next(loans),
            }
        )
        schema_card = Schema(schema=description_c)    
        cards = schema_card.create(iterations = self.records_count)
        return pd.DataFrame(cards)
        
    
    def _generate_ids(self):
        person_ids = self.df_people['id_person'].tolist()
        repeat_count = 0
        ids_for_cards = []
        
        for i in range(len(person_ids)):
            if i % self.similar_people_count == 0 and repeat_count < self.max_repeat_count:
                repeat_count = repeat_count + 1
                
            ids_for_cards = ids_for_cards + [i]*repeat_count
         
        return ids_for_cards
            

    def _generate_people(self):
        people_count = self.similar_people_count * self.max_repeat_count
        ids = iter(range(people_count))
        description_female = (
            lambda: {
            'id_person': next(ids),
            'full_name': self.person.full_name(Gender.FEMALE),
            'gender': 'F',
            }
        )
        description_male = (
            lambda: {
            'id_person': next(ids),
            'full_name': self.person.full_name(Gender.MALE),
            'gender': 'M',
            }
        )
        
        female_count = people_count//2
        male_count = people_count - female_count
        schema_female = Schema(schema=description_female)    
        females = schema_female.create(iterations = female_count)
        
        schema_male = Schema(schema=description_male)    
        males = schema_male.create(iterations = male_count)
        return pd.DataFrame(females + males)
    

if __name__ == '__main__':

    data = DataGenerator()