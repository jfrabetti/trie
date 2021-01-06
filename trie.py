
def strip_punctuation( token ):
    """ Given a token remove any leading or trailing punctuation or white space """
    puncStr = ",.()"

    # TODO: use a regex to strip leading and trailing punctuation
    
    while(1):
        n = len(token)
        token = token.strip(puncStr).strip()
        if len(token) == n:
            break;
    
    return token
    
def tokenize( text ):
    """ Given a block of text remove any punctuation and return  a list of tokens """
    
    # split the text into candidate tokens based on spaces
    tokenL = text.split(" ")
    
    # strip punctuation and white space and drop an resulting empty tokens
    tokenL = [ strip_punctuation(token) for token in tokenL if strip_punctuation(token) ]
    
    return tokenL


def new_node( value ):
    # Create a new node.
    # TODO: Use a class instead of a dictionary
    return {
        "children":{},    # Children nodes.
        "value":value,    # Complete prefix represented by this node
        "term_fl":False   # True if this node represents the end of a complete term.
    }


def insert_node( node, tokenL ):
    """ Insert a term into the trie."""

    # for each token in the term
    for i,token in enumerate(tokenL):
        
        # If the prefix for this term has not yet been inserted ...
        if token not in node['children']:
            # ... then insert it.
            node['children'][token] = new_node(" ".join(tokenL[0:i+1]))
            
        # Traverse to the node assoc'd with 'token'.
        node = node['children'][ token ]

    
    node['value']  = " ".join(tokenL) # Store the complete term in the final node.
    node['term_fl'] = True            # Set 'term_fl' to indicate that this is the termination of a complete term.     
    

def build_trie( termL ):
    """ Given a list of terms  (token lists) create a trie. """

    trie = new_node(None)

    for tokenL in termL:
        insert_node( trie, tokenL )

    return trie

def print_node( node, indent ):
    """ Print the value assoc'd with this node and then the values assoc'd with the children of this node. """
    indentStr = "".join([ " " for i in range(indent) ])
    print(indentStr, node['term_fl'], " value:", node['value'] )

    for k,v in node['children'].items():
        print_node(v,indent+2)

def print_trie( trie ):
    """ Recursively print the trie. """
    print_node( trie, 0 )
    
def find_term(node, tokenL ):
    """ Given a trie, rooted on 'node', locate a matching term beginning on the first token in 'tokenL'
    Returns (matchNode,term_fl) where 'matchNode' is the node matching the last matched token
    and 'term_fl' is true if a complete term was matched. 
    """
    
    matchNode = None
    for token in tokenL:
        if token not in node['children']:
            break

        matchNode = node = node['children'][token]

        
    return (matchNode['value'], matchNode['term_fl']) if matchNode else (None,False)

def find_terms_in_text( trie, text ):
    """ Given a trie, and a string ('text') locate all the encoded in the trie in the string."""

    # Tokenize the text and strip it of punctuation.
    tokenL = tokenize( text )

    print(len(tokenL),tokenL[-1])
    
    for i in range(len(tokenL)):

        match_term, term_fl = find_term( trie, tokenL[i:] )

        if match_term:
            print("Complete" if term_fl else "Partial", "term: ", match_term, "found at token index ", i )
    



if __name__ == "__main__":

    dataText = """
    The operations of each Borrower, and the activities of the officers and directors and, to the knowledge of each Borrower, 
    any Subsidiaries of the Borrowers, employees, agents and representatives of each Borrower, while acting on behalf of such 
    Borrower, and to the knowledge of each Borrower the operations of each Material Project Party in relation to the Project, 
    have been conducted at all times in compliance with all applicable Anti-Money Laundering Laws, Sanctions, and Anti-Corruption 
    Laws. Neither Borrower, nor any Subsidiaries of the Borrowers, nor any officer or director or, to the knowledge of any Borrower, 
    Affiliates, employee, agent or representative of either Borrower has engaged, directly or indirectly, in any activity or conduct 
    which would violate any Anti-Corruption Laws or Anti-Money Laundering Laws. Neither Borrower nor any Subsidiaries of the Borrowers, 
    nor any officer or director or, to the knowledge of any Borrower, Affiliates, employee, agent or representative of either Borrower 
    has engaged, directly or indirectly, in any dealings or transactions with, involving or for the benefit of a Sanctioned Person,
    or in or involving a Sanctioned Country, where such dealings or transactions would violate Sanctions, in the five (5) year period
    immediately preceding the date hereof.
    """

    # Assume the list is already cleaned of punctuation.
    termL = [
        ["Borrower"],
        ["Subsidiaries"],
        ["Material", "Project", "Party"],
        ["Project"],
        ["Project Manager"],
        ["Anti-Money", "Laundering", "Laws" ],
        ["Sanctions"],
        ["Anti-Corruption", "Laws"],
        ["Affiliates"],
        ["Sanctioned", "Person"],
        ["Sanctioned", "Country"],
        ["Person"],
        ["Officer"],
        ["Director"],
        ["Agents"]
    ]




    trie = build_trie(termL)
    print_trie(trie)
    find_terms_in_text(trie,dataText)
    
