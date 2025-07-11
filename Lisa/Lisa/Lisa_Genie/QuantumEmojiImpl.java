import java.util.List;
import org.apache.commons.lang3.tuple.Pair;
import org.apache.commons.lang3.tuple.ImmutablePair;

/**
 * Interface "QuantumEmoji" regroupant toutes les signatures de fonctions
 * et méthodes provenant du code Python équivalent.
 *
 * On y déclare :
 * - Les méthodes liées aux intervalles / picks aléatoires
 * - Les méthodes de build (séquences, expressions logiques)
 * - Les méthodes de mesures (fused emoji, etc.)
 * - Les champs / variables sont ici simulés par des getters / setters
 *   ou des méthodes ad hoc (car Java n'autorise pas de champs dans une interface)
 */
public interface QuantumEmoji {

    /* ========================
       I. Méthodes "globales"
       liées aux intervalles et picks aléatoires
     ========================= */

    /**
     * Retourne un codepoint aléatoire dans la liste d'intervalles (start, end).
     * @param intervals liste d'intervalles [start, end]
     * @return un codepoint entier choisi uniformément
     */
    int pickRandomCp(List<int[]> intervals);

    /**
     * Variante qui parcourt tous les intervalles et renvoie
     * un codepoint aléatoire (ex. version plus évoluée).
     */
    int pickRandomCp2(List<int[]> intervals);

    /**
     * Sélectionne un codepoint "arrow" (par ex. intervalle 0x2190..0x21FF).
     */
    int pickRandomArrow();

    /**
     * Sélectionne un codepoint "genre" (par ex. dans 0x2600..0x26FF).
     */
    int pickRandomGenre();

    /**
     * Sélectionne un codepoint "operateur" (ex. math).
     */
    int pickRandomOperator();

    /* ========================
       II. Méthodes de génération
       (build_random_sequence, build_random_logic_expression, etc.)
     ========================= */

    /**
     * Construit une séquence Unicode "cryptique" (ex. Patterns_2 / Patterns_3),
     * en insérant divers codepoints.
     * @return la séquence finale décodée
     */
    String buildRandomSequence();

    /**
     * Construit une "expression logique" aléatoire, ex. combinant un émoji
     * + un opérateur + parentheses, etc.
     */
    String buildRandomLogicExpression();

    /**
     * Génère un "emoji genré" (ex. woman/man + ZWJ + Variation Selector).
     */
    String buildGenderedEmoji();

    /**
     * Génère un "emoji x-genré" (symbole de genre 0x2600..0x26FF, etc.).
     * @param baseCp un codepoint de base (peut être null pour random)
     */
    String buildXGenderedEmoji(Integer baseCp);

    /* ========================
       III. Mesures sur les séquences
       (fusions, single grapheme, etc.)
     ========================= */

    /**
     * Vérifie si la chaîne s constitue une seule grappe Unicode \X.
     */
    boolean isSingleGrapheme(String s);

    /**
     * Vérifie si la chaîne s constitue exactement deux grappes \X.
     */
    boolean isDoubleGrapheme(String s);

    /**
     * Vérifie si la chaîne s constitue exactement trois grappes \X.
     */
    boolean isTripleGrapheme(String s);

    /**
     * Construire un fused emoji en maxAttempts, si possible (une seule grappe).
     * Sinon renvoie "No fused emoji found".
     */
    String measureFusedEmoji(int maxAttempts);

    /**
     * Tente de construire un fused emoji "exotique",
     * ex. sequences plus complexes (sequence, logic, gendered, etc.).
     */
    String measureFusedEmojiEx(int maxAttempts);

    /* ========================
       IV. Fonctions "hautes"
       (measure_any_emoji, measure_quantumemoji, etc.)
     ========================= */

    /**
     * Renvoie un émoji (ou fallback) au hasard, y compris s'il n'est pas fusionné.
     */
    String measureAnyEmoji();

    /**
     * Réalise la "mesure quantique" globale, modifiant potentiellement
     * plusieurs champs internes (emoji, state, arrow, operator...).
     * Retourne un objet (ou un tuple) décrivant l'état final.
     */
    Object measureQuantumEmoji();

    /* ========================
       V. (Optionnel) Getters / Setters
       Pour simuler les "champs internes"
       (self.emoji, self.state, etc.) de Python
     ========================= */

    /**
     * Renvoie l'emoji courant (string).
     */
    String getEmoji();
    void setEmoji(String emoji);


    String getState();
    void setState(String state);

    String getArrow();
    void setArrow(String arrow);

    String getGender();
    void setGender();

    String getXGender();
    void setXGender();

    String getComplicated();
    void setConplicated();

    String getSimple();
    void setSimple();

    String getOperator();
    void setOperator();

    String getSide();
    void setSide();

    String getOutsde();
    String getInside();

    String getWave();
    void setWave();

    String getWaveErr();
    void setWaveErr();

    /*Quantum Measure*/
    Pair<String, String[]> getMeasure();

}
