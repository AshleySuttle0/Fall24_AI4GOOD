def test_load():
  return 'loaded'
def cond_prob(full_table, the_evidence_column, the_evidence_column_value, the_target_column, the_target_column_value):
  assert the_evidence_column in full_table
  assert the_target_column in full_table
  assert the_evidence_column_value in up_get_column(full_table, the_evidence_column)
  assert the_target_column_value in up_get_column(full_table, the_target_column)

  #your function body below - copy and paste then align with parameter names
  t_subset = up_table_subset(full_table, the_target_column, 'equals', the_target_column_value)
  e_list = up_get_column(t_subset, the_evidence_column)
  p_b_a = sum([1 if v==the_evidence_column_value else 0 for v in e_list])/len(e_list)
  return p_b_a + .01

def cond_probs_product(full_table, evidence_row, target_column, target_column_value):
  assert target_column in full_table
  assert target_column_value in up_get_column(full_table, target_column)
  assert isinstance(evidence_row, list)
  assert len(evidence_row) == len(up_list_column_names(full_table)) - 1   # - 1 because subtracting off the target column from full_table

  #your function body below
  full_table_2 = up_drop_column(full_table, target_column)
  evidence_columns = up_list_column_names(full_table_2)
  evidence_columns

  evidence_values = evidence_row
  evidence_values

  evidence_complete = up_zip_lists(evidence_columns, evidence_values)
  evidence_complete

  cond_prob_list = [cond_prob(full_table, evidence_column, evidence_value, target_column, target_column_value) for evidence_column, evidence_value in evidence_complete]
  cond_probs_product = up_product(cond_prob_list)
  return cond_probs_product

def prior_prob(full_table, the_column, the_column_value):
  assert the_column in full_table
  assert the_column_value in up_get_column(full_table, the_column)

  #your function body below
  flu_table_2 = full_table
  target = the_column
  target_value = the_column_value
  t_list = up_get_column(flu_table_2, target)
  p_a = sum([1 if v==target_value else 0 for v in t_list])/len(t_list)
  return p_a

def naive_bayes(full_table, evidence_row, target_column):
  assert target_column in full_table
  assert isinstance(evidence_row, list)
  assert len(evidence_row) == len(up_list_column_names(full_table)) - 1   # - 1 because subtracting off the target

  #compute P(target=0|...) by using cond_probs_product, finally multiply by P(target=0) using prior_prob
  target_value = 0
  p0 = cond_probs_product(full_table, evidence_row, target_column, target_value) * prior_prob(full_table, target_column, target_value)

  #do same for P(target=1|...)
  target_value = 1
  p1 = cond_probs_product(full_table, evidence_row, target_column, target_value ) * prior_prob(full_table, target_column, target_value)
  
  #Use compute_probs to get 2 probabilities
  neg, pos = compute_probs(p0, p1)
  #return your 2 results in a list
  return [neg, pos]

from sklearn.ensemble import RandomForestClassifier

def run_random_forest(train, test, target, n):
  #target is target column name
  #n is number of trees to use

  assert target in train   #have not dropped it yet
  assert target in test

  #your code below - copy, paste and align from above

  from sklearn.ensemble import RandomForestClassifier
  clf = RandomForestClassifier(n_estimators=n, max_depth=2, random_state=0)

  X = up_drop_column(train, target)
  y = up_get_column(train,target)
  assert isinstance(y,list)
  assert len(y)==len(X)

  clf.fit(X, y)  #builds the trees in the forest - saves you hours of work by hand

  k_feature_table = up_drop_column(test, target)
  k_actuals = up_get_column(test, target)

  probs = clf.predict_proba(k_feature_table)  #Note no need here to transform k_feature_table to list - we can just use the table. Nice.

  assert len(probs)==len(k_actuals)
  assert len(probs[0])==2

  pos_probs = [p for n,p in probs]  #just the positive probabilities

  all_mets = []
  for t in thresholds:
    predictions = [1 if pos>t else 0 for pos in pos_probs]
    pred_act_list = up_zip_lists(predictions, k_actuals)
    mets = metrics(pred_act_list)
    mets['Threshold'] = t
    all_mets = all_mets + [mets]

  metrics_table = up_metrics_table(all_mets)
  metrics_table
  return metrics_table

