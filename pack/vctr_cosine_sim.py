from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def smlrty_prcnt(jd_txt, resume_txt) -> float:
    input_txts = [jd_txt, resume_txt]
    tfidf_vect = TfidfVectorizer()
    tfidf_matrix = tfidf_vect.fit_transform(input_txts)

    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_num = cosine_sim[0, 1]

    cosine_sim_per = float(round(cosine_sim_num, 3))*100.0

    return cosine_sim_per

