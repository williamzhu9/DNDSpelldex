import psycopg2
import logging
import sys
import math

def lambda_handler(event, context):

    #RDS configurations
    user_name = event['USER_NAME']
    password = event['PASSWORD']
    rds_host = event['RDS_HOST']
    db_name = event['DB_NAME']
    port_num = event['PORT']
    spell = event['SPELL']
    level = event['LEVEL']
    SpellMod = event['SPELLMOD']

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
        
    try:
        connection = psycopg2.connect(host = rds_host, 
                                port = port_num, 
                                user = user_name, 
                                password = password, 
                                database = db_name)
        
    except psycopg2.Error as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit(1)
            
    logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")
      
    cursor = connection.cursor()
    # Execute SQL query
    cursor.execute(("select * from SPELLS WHERE Name = '{}'".format(spell)))
    
    # Fetch and process results
    query = cursor.fetchall()

    # Calculating damage
    num_dice, sides = query[0][4].split('d')
    dmg = float(sides)/2 + 0.5
    hit = min((8 + math.ceil(1 + level) + SpellMod), 20)/20
        
    # Concatenates all results for english answer
    results = ("Spell: {} has a range of: {}. It affects a {} for an average damage of {} with a {} % to hit. Expected DPR is {}. Duration is {} and required concentration is {}.".format(query[0][0], query[0][1], query[0][2], int(num_dice) * dmg, hit*100, int(num_dice) * dmg * hit, query[0][5], query[0][6]))

    connection.close()
    return results

    
