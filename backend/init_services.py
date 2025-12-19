from app import app
from models import db, Service

def init_services():
    with app.app_context():
        # Check if services already exist
        if Service.query.count() > 0:
            print("Services already initialized.")
            return

        default_services = [
            {
                "name": "Création de Sites Web",
                "delay": "2-4 semaines",
                "starting_price": "25 000 HTG",
                "roi": "+250%",
                "icon_type": "website",
                "details_anchor": "#website-creation"
            },
            {
                "name": "Photographie",
                "delay": "1-2 jours",
                "starting_price": "8 000 HTG",
                "roi": "+300%",
                "icon_type": "camera",
                "details_anchor": "#photography"
            },
            {
                "name": "Gestion Communautaire",
                "delay": "Mensuel",
                "starting_price": "15 000 HTG/mois",
                "roi": "+400%",
                "icon_type": "community",
                "details_anchor": "#community-management"
            },
            {
                "name": "Design Graphique",
                "delay": "3-7 jours",
                "starting_price": "5 000 HTG",
                "roi": "+180%",
                "icon_type": "design",
                "details_anchor": "#graphic-design"
            },
            {
                "name": "Création de Contenu",
                "delay": "Mensuel",
                "starting_price": "12 000 HTG/mois",
                "roi": "+220%",
                "icon_type": "content",
                "details_anchor": "#content-creation"
            }
        ]

        for s_data in default_services:
            new_service = Service(**s_data)
            db.session.add(new_service)
        
        db.session.commit()
        print(f"Successfully initialized {len(default_services)} services.")

if __name__ == "__main__":
    init_services()
