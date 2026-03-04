# Verivo

**Solution de vote sécurisée pour entreprises, associations et institutions**

---

## Résumé Projet

Verivo est une solution de vote électronique sécurisée visant à garantir :
- ✅ **Inviolabilité** : Aucun vote ne peut être modifié ou supprimé après émission
- ✅ **Audibilité** : Traçabilité complète vérifiable
- ✅ **Anonymat** : Impossible de relier un vote à un électeur spécifique
- ✅ **Accessibilité** : Interface intuitive grand public

---

## Équipe

| Rôle | Nom |
|------|-----|
| Lead Blockchain | Etienne Wallet |
| Lead UX/UI | Solène Mallié |
| Lead Développeur | Arnaud Calvo |
| Développeur | Clément Conand |
| Lead Produit | Philippe Mbongue |

---

## Fonctionnalités Clés

### Accès au scrutin
- ✅ Seuls les personnes ayant le droit de vote peuvent voir le scrutin
- ✅ Le registre des personnes pouvant voter est mis à jour quand le NFT est envoyé

### Base de données
- Table `user` : utilisateurs
- Table `association` : organisations
- Table `rôle` : rôles (organisateur, votant)

### Processus de vote
1. **Inscription** : Création de compte avec wallet associé
2. **Création scrutin** : L'organisateur crée le scrutin et sélectionne les votants
3. **Invitation** : Les personnes sélectionnées reçoivent une invitation à voter
4. **Vote** : Le vote est stocké (étape 1 : en clair, étape 2 : homomorphe)
5. **Confirmation** : Hash de transaction envoyé au votant

### Règles de scrutin
- **Type** : Majorité simple à 1 tour
- **Durée** : Choix par l'organisateur
- **Clôture** : Quand tout le monde a voted OU à la fin du temps défini
- **Irrevocable** : On ne peut pas modifier son vote

### Certification
- Hash de la liste des votants stocké sur blockchain
- NFT de droit de vote (quasi soul-bound) envoyé à chaque votant
- Métadata du scrutin associée au NFT

---

## Pages de l'application

1. **Page d'accueil** : Landing + connexion
2. **Page d'inscription** : Création de compte + wallet
3. **Page création de scrutin** : Paramétrage + sélection des votants
4. **Page vote** : Vote pour les électeurs
5. **Page consultation scrutin** : Résultats (v2)

---

## Vocabulaire (À définir)

Liste de vocabulaire à mettre à disposition des utilisateurs.

---

## Business Model

### Contrainte légale (France)
- Les fédérations sportives devront avoir **50% de participation minimum** aux scrutins
- Vérifiable sur blockchain
- **Grosse opportunité business**

---

## Architecture Technique

### Blockchain
- NFT pour identification des votants
- Hash du registre des votants on-chain
- Étape 1 : Vote stocké en clair
- Étape 2 : Vote homomorphe

### Base de données classique
- `users` : id, wallet_address, email, created_at
- `associations` : id, name, created_at
- `roles` : user_id, association_id, role (organisateur/votant)
- `scrutins` : id, association_id, title, start_date, end_date, status
- `votants_scrutin` : scrutin_id, user_id, wallet_address, email, nft_hash, has_voted

---

## Informations Projet

- **Date de début** : 23-02-2026
- **Statut** : En cours de définition du périmètre
- **Certification** : En perspective avec Alyra

---

## License

À définir...
