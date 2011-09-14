'''Utility functions for credit app.
'''

from django.utils.translation import ugettext as _

def credit_length(obj): 
    return len(obj)

def credit_list(obj, number_to_print=0):
    """Returns formatted list of people for bylines.
    
    Implements "et al." and "and". E.g. "Samuel Johnson, Ingrid Bergman and 
    Lucy Stevens."
    
    Arguments:
    obj -- OrderedCredit GenericRelation 
    number_to_print -- Number of credits to list before "et al." 
    If 0, all authors printed.     

    """
    alist = obj.order_by('position')
    len_alist = len(alist)

    if len_alist == 0:      
        authors=u''
    elif len_alist == 1:        
        authors = unicode(alist[0])
    else:
        if number_to_print == 0 or number_to_print >= len(alist):
            second_last_index = len(alist) - 1
            joining_phrase = unicode(_(u' and '))
            last_name = alist[len(alist)-1].__unicode__()
        else:           
            second_last_index = number_to_print
            joining_phrase = u' ' + _('et al.')
            last_name = ''
                     
        authors = u', '.join([a.__unicode__() \
            for a in alist[0:second_last_index]]) + joining_phrase + \
            last_name

    return authors              
