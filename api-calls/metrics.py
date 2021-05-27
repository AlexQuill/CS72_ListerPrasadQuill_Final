# Imports
from lexical_diversity import lex_div as ld
import pronouncing


# Rhyme Density


def calc_rhyme_density(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    bars = [x.strip() for x in content]

    total_syllables = 0
    rhymed_syllables = 0
    for bar in bars:
        for word in bar.split():
            p = pronouncing.phones_for_word(word)
            if len(p) == 0:
                break
            syllables = pronouncing.syllable_count(p[0])
            total_syllables += syllables
            has_rhyme = False
            for rhyme in pronouncing.rhymes(word):
                if has_rhyme:
                    break
                for idx, r_bar in enumerate(bars):
                    if idx > 4:
                        break
                    if rhyme in r_bar:
                        rhymed_syllables += syllables
                        has_rhyme = True
                        break
    return rhymed_syllables/total_syllables

# Syntactic Complexity

# Online tool?


# Lexical Diversity


def lexical_diversity(corpus, div_type):

    tok = ld.tokenize(corpus)
    print(tok[:10])

    flt = ld.flemmatize(corpus)
    print(flt[:10])

    if div_type == "simple":
        # Simple Text-Type Ratio
        return ld.ttr(flt)
    elif div_type == "root":
        # Root TTR
        return ld.root_ttr(flt)
    elif div_type == "log":
        # Log TTR
        print(ld.log_ttr(flt))
    elif div_type == "mass":
        # Mass TTR
        print(ld.maas_ttr(flt))
    elif div_type == "mean-seg":
        # Mean-segmental TTR
        print(ld.msttr(flt, window_length=25))
    elif div_type == "mov-avg":
        # Moving-Average TTR
        print(ld.mattr(flt, window_length=25))
    elif div_type == "ltd":
        # Lexical textual diversity
        print(ld.mtld(flt))
    elif div_type == "ltd-mov-avg-wrap":
        # LTD moving-average, wrap
        print(ld.mtld_ma_wrap(flt))
    elif div_type == "ltd-mov-avg-bid":
        # LTD moving-average, bidirectional
        print(ld.mtld_ma_bid(flt))
    else:
        print("no type of lexical diversity specified ")
        return None


print(calc_rhyme_density("Lyrics/2pac.txt"))
